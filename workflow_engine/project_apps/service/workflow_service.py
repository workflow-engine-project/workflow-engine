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
    def __init__(self):
        self.workflow_repository = WorkflowRepository()
        self.job_repository = JobRepository()
        self.history_repository = HistoryRepository()
        self.cache = Cache()

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

        # 워크플로우와 작업 목록을 함께 직렬화
        return serialize_workflow(workflow, jobs)

    def get_workflow(self, workflow_uuid):
        workflow = self.workflow_repository.get_workflow(workflow_uuid)

        jobs = self.job_repository.get_job_list(workflow_uuid)

        return serialize_workflow(workflow, jobs)

    @transaction.atomic
    def update_workflow(self, workflow_uuid, workflow_data, jobs_data):
        workflow = self.workflow_repository.update_workflow(
            workflow_uuid=workflow_uuid,
            name=workflow_data.get('name'),
            description=workflow_data.get('description')
        )

        jobs = []
        for job_data in jobs_data:
            job = self.job_repository.update_job(
                job_uuid=job_data.get('uuid'),
                name=job_data.get('name'),
                image=job_data.get('image'),
                parameters=job_data.get('parameters'),
                next_job_names=job_data.get('next_job_names'),
                depends_count=job_data.get('depends_count'),
                timeout=job_data.get('timeout'),
                retries=job_data.get('retries')
            )
            
            jobs.append(job)

        return serialize_workflow(workflow, jobs)

    @transaction.atomic
    def delete_workflow(self, workflow_uuid):
        workflow = self.workflow_repository.get_workflow(workflow_uuid)
        jobs = self.job_repository.get_job_list(workflow_uuid)

        # Workflow 삭제
        self.workflow_repository.delete_workflow(workflow.uuid)

        # Jobs 삭제
        for job in jobs:
            self.job_repository.delete_job(job.uuid)

    def get_workflow_list(self):
        workflows = self.workflow_repository.get_workflow_list()
        workflows_info = []
        for workflow in workflows:
            jobs = self.job_repository.get_job_list(workflow.uuid)
            serialized_workflow = serialize_workflow(workflow, jobs)
            workflows_info.append(serialized_workflow)

        return workflows_info
    
    @with_lock    
    def execute_workflow(self, workflow_uuid):
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
            