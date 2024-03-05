import redis

from django.conf import settings

from functools import wraps

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

def with_lock(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) > 1 and hasattr(args[0], 'workflow_uuid') and isinstance(args[1], str):
            workflow_uuid = args[1]
            lock = redis_client.lock(workflow_uuid)
            with lock.acquire(blocking_timeout=5) as locked:
                if locked:
                    return func(*args, **kwargs)
                else:
                    raise RuntimeError(f"Failed to acquire lock for workflow_uuid: {workflow_uuid}")
        else:
            return func(*args, **kwargs)
    return wrapper
