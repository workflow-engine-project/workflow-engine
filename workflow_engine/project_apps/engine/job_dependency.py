import json

from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded

from project_apps.constants import JOB_STATUS_WAITING
from project_apps.models.cache import Cache
from project_apps.engine.tasks_manager import job_execute


@shared_task
def job_dependency(workflow_uuid, history_uuid):
    try:
        cache = Cache()
        job_list_json = cache.get(workflow_uuid)

        if not job_list_json:
            return {'status': 'error', 'message': 'No jobs found in cache'}

        job_list = json.loads(job_list_json)

        for job_data in job_list:
            if job_data['depends_count'] == 0 and job_data['result'] == JOB_STATUS_WAITING:
                job_execute(workflow_uuid, history_uuid, job_data['uuid'])

        return {'status': 'success', 'message': 'Jobs execution started successfully'}

    except SoftTimeLimitExceeded:
        return {'status': 'error', 'message': 'Soft time limit exceeded during job execution'}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}
