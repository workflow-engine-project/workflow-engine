import json
import threading

from project_apps.constants import HISTORY_STATUS_SUCCESS, HISTORY_STATUS_FAIL, JOB_STATUS_SUCCESS, JOB_STATUS_WAITING
from project_apps.repository.workflow_repository import WorkflowRepository
from project_apps.repository.job_repository import JobRepository
from project_apps.repository.history_repository import HistoryRepository
from project_apps.api.serializers import serialize_workflow
from project_apps.models.cache import Cache
from project_apps.engine.job_dependency import job_dependency
from project_apps.engine.job_execute import job_execute



class WorkflowService:
    def __init__(self):
        self.workflow_repository = WorkflowRepository()
        self.job_repository = JobRepository()

    def create_workflow(self, name, description, jobs_data):
        workflow = self.workflow_repository.create_workflow(
            name=name, 
            description=description
        )

        # 의존성 카운트 계산
        depends_count = {job_data['name']: 0 for job_data in jobs_data}
        for job_data in jobs_data:
            for next_job_name in job_data.get('next_job_names', []):
                if next_job_name in depends_count:
                    depends_count[next_job_name] += 1

        # 작업 정보 생성 및 추가
        jobs_info = []
        for job_data in jobs_data:
            job = self.job_repository.create_job(
                workflow_uuid=workflow.uuid,
                name=job_data['name'],
                image=job_data['image'],
                parameters=job_data.get('parameters', {}),
                next_job_names=job_data.get('next_job_names', []),
                depends_count=depends_count[job_data['name']]
            )

            jobs_info.append({
            'uuid': job.uuid,
            'name': job.name,
            'image': job.image,
            'parameters': job.parameters,
            'depends_count': job.depends_count,
            'next_job_names': job.next_job_names
            })
        
        # 워크플로우 정보 생성
        workflow_info = {
            'uuid': workflow.uuid,
            'name': workflow.name,
            'description': workflow.description
        }
        
        # 워크플로우와 작업 목록을 함께 직렬화
        serialized_workflow = serialize_workflow(workflow_info, jobs_info)

        return serialized_workflow


class WorkflowExecutor:
    '''
    워크플로우 실행을 관리하는 서비스.
    '''
    def __init__(self):
        self.cache = Cache()
        self.lock = threading.Lock()
        
    def find_job_data(self, workflow_uuid, job_uuid):
        '''
        주어진 워크플로우 데이터에서 특정 작업(job)을 찾아 반환.
        찾는 작업이 없으면 None 반환.
        '''
        workflow_data = json.loads(self.cache.get(workflow_uuid))
        for job in workflow_data:
            if job['uuid'] == str(job_uuid):
                return job
        return None

    def update_job_status(self, workflow_uuid, job_uuid, status):
        '''
        특정 작업의 상태를 업데이트하고, 변경된 워크플로우 데이터를 캐시에 저장.
        '''
        with self.lock:
            workflow_data = json.loads(self.cache.get(workflow_uuid))
            for job in workflow_data:
                if job['uuid'] == str(job_uuid):
                    job['result'] = status
                    break
            
            self.cache.set(workflow_uuid, json.dumps(workflow_data))

    def handle_success(self, job_data, workflow_uuid, history_uuid, history_repo):
        updated = False 

        with self.lock:
            workflow_data = json.loads(self.cache.get(workflow_uuid))
            if 'next_job_names' in job_data and job_data['next_job_names']:
                next_job_names_str = job_data['next_job_names'].strip("[]")
                next_job_names = [name.strip(" '\"") for name in next_job_names_str.split(',')]
                for next_job_name in next_job_names:
                    for job in workflow_data:
                        if job['name'] == next_job_name:
                            job['depends_count'] -= 1
                            updated = True
                            if job['depends_count'] == 0:
                                job_execute.apply_async(args=[workflow_uuid, history_uuid, job['uuid']])
                            break

            if updated:
                self.cache.set(workflow_uuid, json.dumps(workflow_data))
        
        self.check_workflow_completion(workflow_uuid, history_uuid, history_repo)

    def handle_failure(self, history_uuid, workflow_uuid, history_repo):
        '''
        작업 실행 실패 시 처리 로직을 수행.
        관련 히스토리를 업데이트하고, 워크플로우 데이터를 캐시에서 삭제.
        '''
        history_repo.update_history_status(history_uuid, HISTORY_STATUS_FAIL)
        self.cache.delete(workflow_uuid)

    def check_workflow_completion(self, workflow_uuid, history_uuid, history_repo):
        '''
        워크플로우의 모든 작업(job)이 성공적으로 완료되었는지 확인.
        모든 작업이 성공적으로 완료되면, 히스토리 상태를 업데이트하고 워크플로우 데이터를 캐시에서 삭제.
        '''
        workflow_data = json.loads(self.cache.get(workflow_uuid))
        completed = True
        for job in workflow_data:
            if job.get('result') != JOB_STATUS_SUCCESS:
                completed = False
                break

        if completed:
            history_repo.update_history_status(history_uuid, HISTORY_STATUS_SUCCESS)
            print("workflow 끝났다!!!")
            self.cache.delete(workflow_uuid)
