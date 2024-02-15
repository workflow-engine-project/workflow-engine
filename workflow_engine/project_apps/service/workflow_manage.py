import threading

import orjson as json

from project_apps.constants import HISTORY_STATUS_FAIL, HISTORY_STATUS_SUCCESS, JOB_STATUS_SUCCESS
from project_apps.engine.tasks_manager import job_dependency
from project_apps.models.cache import Cache
from project_apps.repository.history_repository import HistoryRepository
from project_apps.repository.job_repository import JobRepository


class WorkflowManager:
    '''
    워크플로우 실행을 관리하는 서비스.
    '''
    def __init__(self):
        self.job_repository = JobRepository()
        self.history_repository = HistoryRepository()
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
        '''
        성공한 작업을 처리하고, 해당 작업에 의존하는 다음 작업들의 상태를 업데이트.
        '''
        updated = False 

        with self.lock:
            workflow_data = json.loads(self.cache.get(workflow_uuid))
            next_job_names_str = job_data.next_job_names
            next_job_names = json.loads(next_job_names_str)

            if next_job_names: 
                for next_job_name in next_job_names:
                    for job in workflow_data:
                        if job['name'] == next_job_name:
                            job['depends_count'] -= 1
                            updated = True

            if updated:
                self.cache.set(workflow_uuid, json.dumps(workflow_data))

        if updated:
            job_dependency(workflow_uuid, history_uuid)

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
            self.cache.delete(workflow_uuid)
