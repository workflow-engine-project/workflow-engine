from project_apps.repository.workflow_repository import WorkflowRepository
from project_apps.repository.job_repository import JobRepository
from project_apps.api.serializers import serialize_workflow

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
