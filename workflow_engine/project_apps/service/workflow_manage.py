import orjson as json

from project_apps.constants import HISTORY_STATUS_FAIL, HISTORY_STATUS_SUCCESS, JOB_STATUS_SUCCESS, WORKFLOW_STATUS_FAIL, WORKFLOW_STATUS_SUCCESS
from project_apps.engine.job_terminate import job_terminate
from project_apps.engine.tasks_manager import job_dependency
from project_apps.models.cache import Cache
from project_apps.repository.history_repository import HistoryRepository
from project_apps.repository.job_repository import JobRepository
from project_apps.service.lock_utils import with_lock


class WorkflowManager:
    '''
    워크플로우 실행을 관리하는 서비스.
    '''
    def __init__(self):
        self.job_repository = JobRepository()
        self.history_repository = HistoryRepository()
        self.cache = Cache()
        
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

    @with_lock
    def update_job_status(self, workflow_uuid, job_uuid, status):
        '''
        특정 작업의 상태를 업데이트하고, 변경된 워크플로우 데이터를 캐시에 저장.
        '''
        workflow_data = json.loads(self.cache.get(workflow_uuid))

        workflow_status = self.check_workflow_status(workflow_uuid)
        if workflow_status == WORKFLOW_STATUS_FAIL:
            for job in workflow_data:
                if job['uuid'] == str(job_uuid):
                    job['result'] = status
                    print(f"{job['uuid'], job['result']}")
                    break
            self.cache.set(workflow_uuid, json.dumps(workflow_data))
            return False
        else:
            for job in workflow_data:
                if job['uuid'] == str(job_uuid):
                    job['result'] = status
                    print(f"{job['uuid'], job['result']}")
                    break
            self.cache.set(workflow_uuid, json.dumps(workflow_data))
            return True

    @with_lock
    def update_workflow_status(self, workflow_uuid, status):
        '''
        워크플로우의 상태를 업데이트. 만약 상태가 실패로 업데이트된 경우, 
		실행 중인 모든 도커 컨테이너를 종료
        '''
        self.cache.set(f"{workflow_uuid}_status", status)
        if status == WORKFLOW_STATUS_FAIL:
            running_containers = self.cache.get(f"{workflow_uuid}_running_containers")
            if running_containers:
                for container_id in running_containers:
                    job_terminate.apply_async(args=[container_id])
    
    def check_workflow_status(self, workflow_uuid):
        '''
        워크플로우의 상태를 확인.
        '''
        return self.cache.get(f"{workflow_uuid}_status")

    @with_lock
    def handle_success(self, job_data, workflow_uuid, history_uuid, history_repo):
        '''
        성공한 작업을 처리하고, 해당 작업에 의존하는 다음 작업들의 상태를 업데이트.
        '''
        updated = False 

        workflow_data = json.loads(self.cache.get(workflow_uuid))
        if 'next_job_names' in job_data and job_data['next_job_names']:
            next_job_names_str = job_data['next_job_names'].strip("[]")
            next_job_names = [name.strip(" '\"") for name in next_job_names_str.split(',')]
            for next_job_name in next_job_names:
                for job in workflow_data:
                    if job['name'] == next_job_name:
                        job['depends_count'] -= 1
                        updated = True

        if updated:
            self.cache.set(workflow_uuid, json.dumps(workflow_data))
            job_dependency(workflow_uuid, history_uuid)

        self.check_workflow_completion(workflow_uuid, history_uuid, history_repo)

    def handle_failure(self, history_uuid, workflow_uuid, history_repo):
        '''
        작업 실행 실패 시 처리 로직을 수행.
        워크플로우 실패 상태를 설정하고, 관련 히스토리를 업데이트.
        '''
        self.update_workflow_status(workflow_uuid, WORKFLOW_STATUS_FAIL)
        history_repo.update_history_status(history_uuid, HISTORY_STATUS_FAIL)

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
            self.update_workflow_status(workflow_uuid, WORKFLOW_STATUS_SUCCESS)
            history_repo.update_history_status(history_uuid, HISTORY_STATUS_SUCCESS)

    @with_lock
    def add_container_to_running_list(self, workflow_uuid, container_id):
        '''
        실행 중인 도커 컨테이너의 ID를 워크플로우의 실행중인 컨테이너 목록에 추가.
        '''
        running_containers = self.cache.get(f"{workflow_uuid}_running_containers")
        running_containers.append(container_id)
        self.cache.set(f"{workflow_uuid}_running_containers", running_containers)

    @with_lock
    def remove_container_from_running_list(self, workflow_uuid, container_id):
        '''
        워크플로우의 실행 중인 컨테이너 목록에서 특정 컨테이너의 ID를 제거.
        '''
        running_containers = self.cache.get(f"{workflow_uuid}_running_containers")
        if container_id in running_containers:
            running_containers.remove(container_id)
            self.cache.set(f"{workflow_uuid}_running_containers", running_containers)
