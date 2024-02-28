import orjson as json

from django.db import transaction

from project_apps.repository.scheduling_repository import SchedulingRepository


class SchedulingService:
    def __init__(self):
        self.scheduling_repository = SchedulingRepository()

    def create_scheduling(self, workflow_uuid, scheduled_at, interval, is_active):
        scheduling = self.scheduling_repository.create_scheduling(
            workflow_uuid=workflow_uuid, 
            scheduled_at=scheduled_at,
            interval=interval,
            is_active=is_active,
        )

    @transaction.atomic
    def update_scheduling(self, scheduling_uuid, scheduling_data):
        scheduling = self.scheduling_repository.update_scheduling(
            scheduling_uuid,
            scheduled_at=scheduling_data.get('scheduled_at'),
            interval=scheduling_data.get('interval'),
            is_active=scheduling_data.get('is_active'),
        )
        scheduling_info = {
            'uuid': scheduling.uuid,
            'workflow_uuid': scheduling.workflow_uuid,
            'scheduled_at': scheduling.scheduled_at,
            'interval': scheduling.interval,
            'is_active': scheduling.is_active,
            'created_at': scheduling.created_at,
            'updated_at': scheduling.updated_at,
        }

        return scheduling_info

    @transaction.atomic
    def delete_scheduling(self, scheduling_uuid):
        scheduling = self.scheduling_repository.get_scheduling(scheduling_uuid)

        # scheduling 삭제
        self.scheduling_repository.delete_scheduling(scheduling.uuid)
