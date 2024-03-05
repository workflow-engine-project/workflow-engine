import orjson as json
from django.db import transaction

from project_apps.api.serializers import serialize_workflow
from project_apps.constants import JOB_STATUS_WAITING, WORKFLOW_STATUS_RUNNING
from project_apps.engine.tasks_manager import job_dependency
from project_apps.models.cache import Cache
from project_apps.repository.history_repository import HistoryRepository
from project_apps.repository.job_repository import JobRepository
from project_apps.repository.workflow_repository import WorkflowRepository
from project_apps.service.lock_utils import with_lock


class WorkflowService:
    '''
    Workflow 정보를 관리하는 서비스.
    '''
    def __init__(self):
        self.workflow_repository = WorkflowRepository()
        self.job_repository = JobRepository()
        self.history_repository = HistoryRepository()
        self.cache = Cache()

    def create_workflow(self, name, description, jobs_data):
        '''
        입력 받은 데이터를 바탕으로 의존성 카운트를 계산하고, 
        Workflow와 Job 리스트를 생성하고 그 결과를 반환한다.
        '''
        workflow = self.workflow_repository.create_workflow(
            name=name, 
            description=description
        )

        depends_count = {job_data['name']: 0 for job_data in jobs_data}
        for job_data in jobs_data:
            for next_job_name in job_data.get('next_job_names', []):
                if next_job_name in depends_count:
                    depends_count[next_job_name] += 1

        jobs = []
        for job_data in jobs_data:
            job = self.job_repository.create_job(
                workflow_uuid=workflow.uuid,
                name=job_data['name'],
                image=job_data['image'],
                parameters=job_data.get('parameters', {}),
                next_job_names=job_data.get('next_job_names', []),
                depends_count=depends_count[job_data['name']],
                timeout=job_data.get('timeout', 0),
                retries=job_data.get('retries', 0)
            )

            jobs.append(job)

        return serialize_workflow(workflow, jobs)

    def get_workflow(self, workflow_uuid):
        '''
        입력 받은 Workflow와 그에 포함된 Job 리스트를 반환한다.
        '''
        workflow = self.workflow_repository.get_workflow(workflow_uuid)

        jobs = self.job_repository.get_job_list(workflow_uuid)

        return serialize_workflow(workflow, jobs)

    @transaction.atomic
    def update_workflow(self, workflow_uuid, workflow_data, jobs_data):
        '''
        입력 받은 Workflow와 Job 리스트를 주어진 데이터로 수정하고, 
        그 결과를 반환한다.
        '''
        workflow = self.workflow_repository.update_workflow(
            workflow_uuid=workflow_uuid,
            name=workflow_data.get('name'),
            description=workflow_data.get('description')
        )

        # 의존성 카운트 계산
        depends_count = {job_data['name']: 0 for job_data in jobs_data}
        for job_data in jobs_data:
            for next_job_name in job_data.get('next_job_names', []):
                if next_job_name in depends_count:
                    depends_count[next_job_name] += 1

        jobs = []
        for job_data in jobs_data:
            job = self.job_repository.update_job(
                job_uuid=job_data.get('uuid'),
                name=job_data.get('name'),
                image=job_data.get('image'),
                parameters=job_data.get('parameters'),
                next_job_names=job_data.get('next_job_names'),
                depends_count=depends_count[job_data['name']],
                timeout=job_data.get('timeout'),
                retries=job_data.get('retries')
            )
            
            jobs.append(job)

        return serialize_workflow(workflow, jobs)

    @transaction.atomic
    def delete_workflow(self, workflow_uuid):
        '''
        입력 받은 Workflow와 Job 리스트를 삭제한다.
        '''
        workflow = self.workflow_repository.get_workflow(workflow_uuid)

        if isinstance(workflow, dict):
            return False

        jobs = self.job_repository.get_job_list(workflow_uuid)

        self.workflow_repository.delete_workflow(workflow.uuid)

        for job in jobs:
            self.job_repository.delete_job(job.uuid)

        return True

    def get_workflow_list(self):
        '''
        모든 Workflow의 정보와 각각의 Job 리스트를 반환한다.
        '''
        workflows = self.workflow_repository.get_workflow_list()
        workflows_info = []
        for workflow in workflows:
            jobs = self.job_repository.get_job_list(workflow.uuid)
            serialized_workflow = serialize_workflow(workflow, jobs)
            workflows_info.append(serialized_workflow)

        return workflows_info
    
    @with_lock
    def execute_workflow(self, workflow_uuid):
        '''
        실행 요청을 받은 Workflow를 캐싱, 실행 History 생성 
        및 Job 의존성을 계산하여 Workflow 실행을 준비한다.
        '''
        self.cache.delete(f"{workflow_uuid}")
        self.cache.delete(f"{workflow_uuid}_status")
        self.cache.delete(f"{workflow_uuid}_running_containers")

        job_list = self.job_repository.get_job_list(workflow_uuid).values()
        for job in job_list:
            job['result'] = JOB_STATUS_WAITING
            job['uuid'] = str(job['uuid'])

        if job_list:
            job_list_json = json.dumps(list(job_list))
            self.cache.set(workflow_uuid, job_list_json)            
            self.cache.set(f"{workflow_uuid}_status", WORKFLOW_STATUS_RUNNING)
            self.cache.set(f"{workflow_uuid}_running_containers", [])

            history = self.history_repository.create_history(workflow_uuid)
            job_dependency(workflow_uuid, history.uuid)

            return True
        else:
            return False
