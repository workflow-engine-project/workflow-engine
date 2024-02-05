from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

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
        try:
            job = Job.objects.get(uuid=job_uuid)
            return job
        except ObjectDoesNotExist:
            return {'status': 'error', 'message': 'Workflow not found'}
        except MultipleObjectsReturned:
            return {'status': 'error', 'message': 'Multiple workflows found with the same UUID'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def update_job(self, job_uuid, name, image, parameters, next_job_names, depends_count):
        job = Job.objects.get(uuid=job_uuid)

        for arg, val in locals().items():
            if val is not None:
                setattr(job, arg, val)
        job.save()

        return job

    def delete_job(self, job_uuid):
        try:
            job = Job.objects.get(uuid=job_uuid)
            job.delete()
            return {'status': 'success', 'message': 'job deleted successfully'}
        except ObjectDoesNotExist:
            return {'status': 'error', 'message': 'job not found'}
        except MultipleObjectsReturned:
            return {'status': 'error', 'message': 'Multiple jobs found with the same UUID'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_job_list(self, workflow_uuid):
        job_list = Job.objects.filter(workflow_uuid = workflow_uuid)
        return list(job_list.values())
