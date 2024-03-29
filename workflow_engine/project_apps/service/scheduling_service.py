from django.db import transaction
from django.utils import timezone

from project_apps.api.serializers import serialize_scheduling
from project_apps.engine.scheduling_execute import execute_scheduling
from project_apps.repository.scheduling_repository import SchedulingRepository


class SchedulingService:
    '''
    Scheduling 정보를 관리하는 서비스.
    '''
    def __init__(self):
        self.scheduling_repository = SchedulingRepository()

    def create_scheduling(self, workflow_uuid, scheduled_at, interval, repeat_count):
        '''
        입력 받은 데이터를 바탕으로 Scheduling을 생성한다.
        '''
        scheduling = self.scheduling_repository.create_scheduling(
            workflow_uuid=workflow_uuid, 
            scheduled_at=scheduled_at,
            interval=interval,
            repeat_count=repeat_count
        )

        return serialize_scheduling(scheduling)

    def get_scheduling(self, scheduling_uuid):
        '''
        입력 받은 Scheduling을 반환한다.
        '''
        scheduling = self.scheduling_repository.get_scheduling(scheduling_uuid)

        return serialize_scheduling(scheduling)

    def get_workflow_scheduling_list(self, workflow_uuid):
        '''
        특정 워크플로우에 종속된 Scheduling의 정보를 반환한다.
        '''
        schedulings = self.scheduling_repository.get_workflow_scheduling_list(workflow_uuid)
        schedulings_info = []
        for scheduling in schedulings:
            schedulings_info.append({
                'uuid': scheduling['uuid'],
                'workflow_uuid': scheduling['workflow_uuid'],
                'scheduled_at': scheduling['scheduled_at'],
                'interval': scheduling['interval'],
                'repeat_count': scheduling['repeat_count'],
                'is_active': scheduling['is_active'],
                'created_at': scheduling['created_at'],
                'updated_at': scheduling['updated_at'],
            })

        return schedulings_info
    
    def get_scheduling_list(self):
        '''
        모든 Scheduling의 정보를 반환한다.
        '''
        schedulings = self.scheduling_repository.get_scheduling_list()
        schedulings_info = []
        for scheduling in schedulings:
            schedulings_info.append({
                'uuid': scheduling['uuid'],
                'workflow_uuid': scheduling['workflow_uuid'],
                'scheduled_at': scheduling['scheduled_at'],
                'interval': scheduling['interval'],
                'repeat_count': scheduling['repeat_count'],
                'is_active': scheduling['is_active'],
                'created_at': scheduling['created_at'],
                'updated_at': scheduling['updated_at'],
            })

        return schedulings_info

    @transaction.atomic
    def update_scheduling(self, scheduling_uuid, scheduling_data):
        '''
        입력 받은 Scheduling을 전송 받은 데이터로 수정한다.
        '''
        scheduling = self.scheduling_repository.get_scheduling(scheduling_uuid)

        if scheduling.is_active:
            return False, "스케줄링이 이미 활성화되었으므로 업데이트할 수 없습니다."
         
        scheduling = self.scheduling_repository.update_scheduling(
            scheduling_uuid,
            scheduled_at=scheduling_data.get('scheduled_at'),
            interval=scheduling_data.get('interval'),
            repeat_count=scheduling_data.get('repeat_count'),
        )

        return True, serialize_scheduling(scheduling)

    @transaction.atomic
    def delete_scheduling(self, scheduling_uuid):
        '''
        입력 받은 Scheduling을 삭제한다.
        '''
        scheduling = self.scheduling_repository.get_scheduling(scheduling_uuid)

        self.scheduling_repository.delete_scheduling(scheduling.uuid)
        
    @transaction.atomic
    def activate_scheduling(self, scheduling_uuid):
        '''
        입력 받은 Scheduling을 활성화한다.
        '''
        scheduling = self.scheduling_repository.get_scheduling(scheduling_uuid)

        if scheduling.is_active:
            return False, "스케줄링이 이미 활성화되어있습니다"
            
        if scheduling.scheduled_at and scheduling.scheduled_at < timezone.now():
            return False, "스케줄링 예정된 시간이 지났습니다."
            
        success, message = self.scheduling_repository.activate_scheduling(scheduling_uuid)
        if scheduling.scheduled_at:
            delay = (scheduling.scheduled_at - timezone.now()).total_seconds()
            execute_scheduling.apply_async((scheduling_uuid,), countdown=delay)
        else:
            execute_scheduling.delay(scheduling_uuid)

        return success, message

    @transaction.atomic
    def deactivate_scheduling(self, scheduling_uuid):
        '''
        입력 받은 Scheduling을 비활성화한다.
        '''
        scheduling = self.scheduling_repository.get_scheduling(scheduling_uuid)

        if not scheduling.is_active:
            return False, "스케줄링이 이미 비활성화되어 있습니다."

        success, message = self.scheduling_repository.deactivate_scheduling(scheduling_uuid)

        return success, message
