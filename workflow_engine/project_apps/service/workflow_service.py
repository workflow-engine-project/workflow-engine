import ast
import orjson as json
import uuid

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
        # Job 이름의 중복 여부 판별
        jobs_name = []

        for job_data in jobs_data:
            if job_data.get('name') in jobs_name:
                raise ValueError(f"Multiple Jobs found with the same name {job_data.get('name')}")
            else:
                jobs_name.append(job_data.get('name'))

        # 의존성이 걸린 작업의 실존 여부 판별
        for job_data in jobs_data:
            for next_job_name in job_data.get('next_job_names', []):
                if next_job_name not in jobs_name:
                    raise ValueError (f"Job '{next_job_name}' referenced in next_job_names does not exist")

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
        existing_jobs = self.job_repository.get_job_list(workflow_uuid)
        existing_jobs_dict = {job.uuid: job for job in existing_jobs}

        name_uuid_mapping = {job.name: job.uuid for job in existing_jobs}

        jobs_name = [job.name for job in existing_jobs]

        job_updates = {}
        depend_updates = {}

        for job_data in jobs_data:
            job_uuid = uuid.UUID(job_data['uuid'])
            job_name = job_data['name']

            current_job = existing_jobs_dict.get(job_uuid)

            new_next_job_names = job_data.get('next_job_names', [])
            for next_job_name in new_next_job_names:
                if next_job_name not in jobs_name:
                    raise ValueError(f"'{job_name}' references '{next_job_name}' in its next_job_names, but '{next_job_name}' does not exist")
        
            old_next_job_names = ast.literal_eval(current_job.next_job_names) if current_job else []

            for removed_name in set(old_next_job_names) - set(new_next_job_names):
                removed_uuid = name_uuid_mapping.get(removed_name)
                if removed_uuid:
                    depend_updates[removed_uuid] = depend_updates.get(removed_uuid, 0) - 1

            for added_name in set(new_next_job_names) - set(old_next_job_names):
                added_uuid = name_uuid_mapping.get(added_name)
                if added_uuid:
                    depend_updates[added_uuid] = depend_updates.get(added_uuid, 0) + 1

            job_updates[job_uuid] = {
                "uuid": job_uuid,
                "name": job_name,
                "image": job_data['image'],
                "parameters": job_data['parameters'],
                "next_job_names": new_next_job_names,
                "timeout": job_data.get('timeout', 0),
                "retries": job_data.get('retries', 0),
                "depends_count": existing_jobs_dict[job_uuid].depends_count if job_uuid in existing_jobs_dict else 0
            }

        for job_uuid, count_change in depend_updates.items():
            new_count = max(existing_jobs_dict[job_uuid].depends_count+count_change, 0)
            if job_uuid in job_updates:
                job_updates[job_uuid]["depends_count"] = new_count
            else:
                if job_uuid in existing_jobs_dict:
                    next_job_names = ast.literal_eval(existing_jobs_dict[job_uuid].next_job_names)
                    job_updates[job_uuid] = {
                        "uuid": existing_jobs_dict[job_uuid].uuid,
                        "name": existing_jobs_dict[job_uuid].name,
                        "image": existing_jobs_dict[job_uuid].image,
                        "parameters": existing_jobs_dict[job_uuid].parameters,
                        "next_job_names": next_job_names,
                        "timeout": existing_jobs_dict[job_uuid].timeout,
                        "retries": existing_jobs_dict[job_uuid].retries,
                        "depends_count": new_count
                    }

        update_jobs = []
        for job_uuid, update_data in job_updates.items():
            updated_job = self.job_repository.update_job(
                job_uuid=update_data['uuid'],
                name=update_data['name'],
                image=update_data['image'],
                parameters=update_data['parameters'],
                next_job_names=update_data['next_job_names'],
                depends_count=update_data['depends_count'],
                timeout=update_data['timeout'],
                retries=update_data['retries']
            )
            update_jobs.append(updated_job)

        workflow_info = self.workflow_repository.update_workflow(
            workflow_uuid=workflow_uuid,
            name=workflow_data.get('name', ''),
            description=workflow_data.get('description', '')
        )

        return serialize_workflow(workflow_info, update_jobs)
    

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
