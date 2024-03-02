def serialize_workflow(workflow_info, jobs_data):
    '''
    workflow 해당 workflow 속한 job 데이터 직렬화
    '''
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
