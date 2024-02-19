import docker, json
from celery import shared_task
from requests.exceptions import ReadTimeout, ConnectionError

from project_apps.constants import JOB_STATUS_RUNNING, JOB_STATUS_SUCCESS, JOB_STATUS_FAIL
from project_apps.repository.history_repository import HistoryRepository
from project_apps.service.workflow_manage import WorkflowManager


@shared_task
def job_execute(workflow_uuid, history_uuid, job_uuid):
    client = docker.from_env()
    workflow_manager = WorkflowManager()
    history_repo = HistoryRepository()

    job_data = workflow_manager.find_job_data(workflow_uuid, job_uuid)
    
    if not job_data:    
        return

    try:
        workflow_manager.update_job_status(workflow_uuid, job_uuid, JOB_STATUS_RUNNING)
        image = client.images.pull(job_data['image'])
        environment = json.loads(job_data.get('parameters'))
        container = client.containers.run(image, detach=True, environment=environment)
        result = container.wait(timeout=60)
        
        if result['StatusCode'] == 0:
            workflow_manager.update_job_status(workflow_uuid, job_uuid, JOB_STATUS_SUCCESS)
            workflow_manager.handle_success(job_data, workflow_uuid, history_uuid, history_repo)
        else:
            workflow_manager.handle_failure(history_uuid, workflow_uuid, history_repo)
            
    except (ReadTimeout, ConnectionError) as e:
        workflow_manager.update_job_status(workflow_uuid, job_uuid, JOB_STATUS_FAIL)
        workflow_manager.handle_failure(history_uuid, workflow_uuid, history_repo)

    except Exception as e:
        workflow_manager.handle_failure(history_uuid, workflow_uuid, history_repo)
