from models import Job

class JobRepository:
    def create_job(self, workflow_uuid, name, image, parameters, next_job_uuid, depends_count):
        pass

    def get_job(self, job_uuid):
        pass
    
    def update_job(self, job_uuid, **kwargs):
        # TODO: 업데이트 필드 확정
        # TODO: 확정된 필드를 매개변수로 전부 넣어주고 default 값을 None으로 설정하여 모든 필드 값을 받도록 설정
        pass

    def delete_job(self, job_uuid):
        pass
