import docker
from celery import shared_task


@shared_task
def job_terminate(container_id):
    '''
    입력받은 도커 컨테이너를 종료한다.
    '''
    client = docker.from_env()
    try:
        container = client.containers.get(container_id)
        if container.status == 'running':
            container.kill()

    except Exception as e:
        print(f"Error terminating container {container_id}: {e}")
