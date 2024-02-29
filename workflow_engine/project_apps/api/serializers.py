def serialize_workflow(workflow_info, jobs_data):
    '''
    workflow 해당 workflow 속한 job 데이터 직렬화
    '''
    serialized_jobs = []
    for job_data in jobs_data:
        serialized_job = {
            "uuid": job_data['uuid'],
            "workflow_uuid": workflow_info['uuid'],
            "name": job_data['name'],
            "image": job_data.get('image', ''),
            "parameters": job_data.get('parameters', {}),
            "next_job_names": job_data.get('next_job_names', []),
            "depends_count": job_data.get('depends_count', 0),
            "timeout": job_data.get('timeout', 0),
            "retries": job_data.get('retries', 0)
        }
        serialized_jobs.append(serialized_job)

    serialized_workflow = {
        "workflow": {
            "uuid": workflow_info['uuid'],
            "name": workflow_info['name'],
            "description": workflow_info['description'],
            "jobs": serialized_jobs
        }
    }

    return serialized_workflow
