from project_apps.models import Scheduling


class SchedulingRepository:
    def create_scheduling(self, workflow_uuid, scheduled_at, interval, is_active):
        scheduling = Scheduling.objects.create(workflow_uuid=workflow_uuid, scheduled_at=scheduled_at, interval=interval, is_active=is_active)
        return scheduling
