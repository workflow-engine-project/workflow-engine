from django.db import IntegrityError

from project_apps.models import Job


class JobRepository:
    '''
    Job 정보를 관리하는 리포지토리.
    '''
    def create_job(self, workflow_uuid, name, image, parameters, next_job_names, depends_count=0, timeout=0, retries=0):
        '''
        Job 정보를 생성한다.
        '''
        try:
            job = Job.objects.create(
                workflow_uuid=workflow_uuid,
                name=name,
                image=image,
                parameters=parameters,
                next_job_names=next_job_names,
                depends_count=depends_count,
                timeout=timeout,
                retries=retries
            )
            
            return job
        except Exception as e:
            raise ValueError(str(e))

    def get_job(self, job_uuid):
        '''
        일치하는 Job 정보를 반환한다.
        '''
        try:
            job = Job.objects.get(uuid=job_uuid)
            return job
        except Exception as e:
            raise ValueError(str(e))

    def update_job(self, job_uuid, name, image, parameters, next_job_names, depends_count, timeout, retries):
        '''
        일치하는 Job을 인자에 주어진 정보로 수정한다.
        '''
        try:
            job = Job.objects.get(uuid=job_uuid)

            for arg, val in locals().items():
                if val is not None:
                    setattr(job, arg, val)
            job.save()

            return job
        except IntegrityError:
            raise ValueError(f'Job with name {job.name} already exists.')
        except Exception as e:
            raise ValueError(str(e))

    def delete_job(self, job_uuid):
        '''
        일치하는 Job 정보를 삭제한다.
        '''
        try:
            job = Job.objects.get(uuid=job_uuid)
            job.delete()
            return {'status': 'success', 'message': 'job deleted successfully'}
        except Exception as e:
            raise ValueError(str(e))

    def get_job_list(self, workflow_uuid):
        '''
        일치하는 Workflow의 모든 Job 리스트를 반환한다.
        '''
        job_list = Job.objects.filter(workflow_uuid=workflow_uuid)
        return job_list
