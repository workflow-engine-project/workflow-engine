def serialize_workflow(workflow_info, jobs_data):
    '''
    입력받은 Workflow와 Job 모델 객체를 직렬화한다.
    '''
    if type(workflow_info) is dict:
        raise ValueError("요청받은 workflow 정보의 형식이 올바르지 않습니다.")
    
    if type(jobs_data[0]) is dict:
        raise ValueError("요청받은 job 정보의 형식이 올바르지 않습니다.")
    
    serialized_jobs = []
    for job_data in jobs_data:
        serialized_job = {
            'uuid': job_data.uuid,
            'name': job_data.name,
            'image': job_data.image,
            'parameters': job_data.parameters,
            'next_job_names': job_data.next_job_names,
            'depends_count': job_data.depends_count,
            'timeout': job_data.timeout,
            'retries': job_data.retries
        }
        serialized_jobs.append(serialized_job)

    serialized_workflow = {
        'uuid': workflow_info.uuid,
        'name': workflow_info.name,
        'description': workflow_info.description,
        'created_at': workflow_info.created_at,
        'updated_at': workflow_info.updated_at,
        'jobs': serialized_jobs
    }

    return serialized_workflow

def serialize_scheduling(scheduling_info):
    if type(scheduling_info) is dict:
        raise ValueError("요청받은 scheduling 정보의 형식이 올바르지 않습니다.")
    
    serialized_scheduling = {
        'uuid': scheduling_info.uuid,
        'scheduled_at': scheduling_info.scheduled_at,
        'interval': scheduling_info.interval,
        'repeat_count': scheduling_info.repeat_count,
        'is_active': scheduling_info.is_active,
        'created_at': scheduling_info.created_at,
        'updated_at': scheduling_info.updated_at
    }

    return serialized_scheduling
