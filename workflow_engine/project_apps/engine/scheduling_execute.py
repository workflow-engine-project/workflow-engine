from celery import shared_task
from django.utils import timezone

from project_apps.models.cache import Cache
from project_apps.repository.scheduling_repository import SchedulingRepository
from project_apps.service.workflow_service import WorkflowService

cache = Cache()
scheduling_repo = SchedulingRepository()
workflow_service = WorkflowService()

@shared_task
def execute_scheduling(scheduling_uuid):
    scheduling = scheduling_repo.get_scheduling(scheduling_uuid)

    execute_scheduling_workflow(scheduling)

    if not scheduling.interval:
        scheduling.is_active = False
        print(f"{scheduling_uuid} 스케줄링 마지막 작업 완료 후 종료됩니다.")
        scheduling.save()
    else:
        manage_repeated_execution(scheduling)


def execute_scheduling_workflow(scheduling):
    workflow_service.execute_workflow(scheduling.workflow_uuid)
    print(f"스케줄링 작업 실행: {scheduling.uuid} at {timezone.now()}")


def manage_repeated_execution(scheduling):
    repeat_key = f"scheduling:{scheduling.uuid}:repeat_count"
    repeat_count = cache.get(repeat_key)

    if repeat_count is None:
        cache.set(repeat_key, scheduling.repeat_count)
        repeat_count = scheduling.repeat_count
    else:
        repeat_count = int(repeat_count) - 1
        cache.set(repeat_key, repeat_count)

    if repeat_count <= 0:
        scheduling.is_active = False
        scheduling.save()
        print(f"{scheduling.uuid} 스케줄링 마지막 작업 완료 후 종료됩니다.")
        cache.delete(repeat_key)
    else:
        countdown = scheduling.interval.total_seconds()
        execute_scheduling.apply_async((scheduling.uuid,), countdown=countdown)
