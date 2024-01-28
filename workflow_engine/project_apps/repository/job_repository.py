from project_apps.models import Job

class JobRepository:
    def create_job(self, workflow_uuid, name, image, parameters, next_job_names, depends_count=0):
        job = Job.objects.create(
            workflow_uuid=workflow_uuid,
            name=name,
            image=image,
            parameters=parameters,
            next_job_names=next_job_names,
            depends_count=depends_count
        )
        
        return job
        
    def get_job(self, job_uuid):
        pass

    def update_job(self, job_uuid, **kwargs):
        # TODO: 업데이트 필드 확정
        # TODO: 확정된 필드를 매개변수로 전부 넣어주고 default 값을 None으로 설정하여 모든 필드 값을 받도록 설정
        pass

    def delete_job(self, job_uuid):
        Job.objects.get(uuid=job_uuid).delete()

    def get_job_list(self, workflow_uuid):
        return Job.objects.filter(workflow_uuid = workflow_uuid)
