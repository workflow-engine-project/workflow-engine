from celery import current_app


def job_execute(workflow_uuid, history_uuid, job_uuid):
    '''
    job을 실제 수행하는 celery task
    '''
    current_app.send_task('project_apps.engine.job_execute.job_trial', args=[workflow_uuid, history_uuid, job_uuid])


def job_dependency(workflow_uuid, history_uuid):
    '''
    job 의존성 관련 celery task
    '''
    current_app.send_task('project_apps.engine.job_dependency.job_dependency', args=[workflow_uuid, history_uuid])
