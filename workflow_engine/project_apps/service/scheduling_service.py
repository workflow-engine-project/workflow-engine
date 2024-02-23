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

        # 스케줄링 정보 생성
        scheduling_info = {
            'uuid': scheduling.uuid,
            'workflow_uuid': scheduling.workflow_uuid,
            'scheduled_at': scheduling.scheduled_at,
            'interval': scheduling.interval,
            'is_active': scheduling.is_active,
        }

        return scheduling_info
