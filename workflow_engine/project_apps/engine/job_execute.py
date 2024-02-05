import docker
from celery import shared_task
from requests.exceptions import ReadTimeout, ConnectionError

from project_apps.constants import JOB_STATUS_RUNNING, JOB_STATUS_SUCCESS, JOB_STATUS_FAIL
from project_apps.repository.history_repository import HistoryRepository


@shared_task
def job_execute(workflow_uuid, history_uuid, job_uuid):
    client = docker.from_env()
    from project_apps.service.workflow_service import WorkflowExecutor
    workflow_executor = WorkflowExecutor()
    history_repo = HistoryRepository()

    job_data = workflow_executor.find_job_data(workflow_uuid, job_uuid)
    
    if not job_data:    
        return

    try:
        workflow_executor.update_job_status(workflow_uuid, job_uuid, JOB_STATUS_RUNNING)
        image = client.images.pull(job_data['image'])
        container = client.containers.run(image, detach=True)
        # container = client.containers.run(image, detach=True, environment=job_data.get('parameters', {}))
        result = container.wait(timeout=60)
        
        if result['StatusCode'] == 0:
            workflow_executor.update_job_status(workflow_uuid, job_uuid, JOB_STATUS_SUCCESS)
            workflow_executor.handle_success(job_data, workflow_uuid, history_uuid, history_repo)
        else:
            workflow_executor.handle_failure(history_uuid, workflow_uuid, history_repo)
            
    except (ReadTimeout, ConnectionError) as e:
        workflow_executor.update_job_status(workflow_uuid, job_uuid, JOB_STATUS_FAIL)
        workflow_executor.handle_failure(history_uuid, workflow_uuid, history_repo)

    except Exception as e:
        workflow_executor.handle_failure(history_uuid, workflow_uuid, history_repo)
