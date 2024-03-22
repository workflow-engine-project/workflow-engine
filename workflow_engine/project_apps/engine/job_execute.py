from requests.exceptions import ReadTimeout, ConnectionError

import docker, orjson as json
from docker.errors import ImageNotFound, APIError
from celery import shared_task

from project_apps.constants import JOB_STATUS_RUNNING, JOB_STATUS_SUCCESS, JOB_STATUS_FAIL, WORKFLOW_STATUS_FAIL
from project_apps.service.workflow_manage import WorkflowManager


@shared_task
def job_trial(workflow_uuid, history_uuid, job_uuid):
    '''
    최대 지정된 retries 수만큼 job을 수행 시도하고, 결과에 따라 처리한다.
    '''
    workflow_manager = WorkflowManager()

    job_data = workflow_manager.find_job_data(workflow_uuid, job_uuid)
    if not job_data:
        return
    
    retries = job_data['retries']
    for _ in range(retries+1):
        result = job_execute(workflow_uuid, history_uuid, job_uuid)
        if result is not None:
            return
    
    workflow_manager.update_job_status(workflow_uuid, job_uuid, JOB_STATUS_FAIL)
    workflow_manager.handle_failure(workflow_uuid, history_uuid)
    
def job_execute(workflow_uuid, history_uuid, job_uuid):
    '''
    입력 받은 Job을 제한된 timeout 내에 수행하고, 결과에 따라 처리한다.
    '''
    client = docker.from_env()
    workflow_manager = WorkflowManager()

    if workflow_manager.check_workflow_status(workflow_uuid) == WORKFLOW_STATUS_FAIL:
        return False

    job_data = workflow_manager.find_job_data(workflow_uuid, job_uuid)
    if not job_data:
        return False

    try:
        if not workflow_manager.update_job_status(workflow_uuid, job_uuid, JOB_STATUS_RUNNING):
            return False
        image = client.images.pull(job_data['image'])
        parameters = job_data.get('parameters', '{}')
        environment = json.loads(parameters.replace("'", "\""))
        timeout = job_data['timeout']
        if not timeout:
            timeout = 10
        
        container = client.containers.run(image, detach=True, environment=environment)
        workflow_manager.add_container_to_running_list(workflow_uuid, container.id)
        result = container.wait(timeout=timeout)

        if result['StatusCode'] == 0:
            if not workflow_manager.update_job_status(workflow_uuid, job_uuid, JOB_STATUS_SUCCESS):
                return False
            workflow_manager.handle_success(job_data, workflow_uuid, history_uuid)
            workflow_manager.remove_container_from_running_list(workflow_uuid, container.id)
            container.remove()
            return True
        else:
            return None

    except (ReadTimeout, ConnectionError, ImageNotFound, APIError) as e:
        return None

    except Exception as e:
        return None
