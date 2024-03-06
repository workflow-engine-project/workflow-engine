from datetime import timedelta

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.utils.dateparse import parse_datetime

from project_apps.models import Scheduling, Workflow


class SchedulingRepository:
    '''
    Scheduling 정보를 관리하는 리포지토리.
    '''
    def create_scheduling(self, workflow_uuid, scheduled_at, interval, repeat_count):
        '''
        Scheduling 정보를 생성한다.
        '''
        try:
            workflow = Workflow.objects.get(uuid=workflow_uuid)

            parse_scheduled_at = parse_datetime(scheduled_at) if scheduled_at else None
            parse_interval = timedelta(**interval) if interval else None

            scheduling = Scheduling.objects.create(
                workflow_uuid=workflow_uuid, 
                scheduled_at=parse_scheduled_at, 
                interval=parse_interval, 
                repeat_count=repeat_count
            )
            return scheduling
        except ObjectDoesNotExist:
            return {'status': 'error', 'message': 'Workflow not found'}
        except MultipleObjectsReturned:
            return {'status': 'error', 'message': 'Multiple workflows found with the same UUID'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_scheduling(self, scheduling_uuid):
        '''
        일치하는 Scheduling 정보를 반환한다.
        '''
        try:
            scheduling = Scheduling.objects.get(uuid=scheduling_uuid)
            return scheduling
        except ObjectDoesNotExist:
            return {'status': 'error', 'message': 'Scheduling not found'}
        except MultipleObjectsReturned:
            return {'status': 'error', 'message': 'Multiple schedulings found with the same UUID'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_workflow_scheduling_list(self, workflow_uuid):
        '''
        특정 워크플로우에 종속된 Scheduling의 리스트를 반환한다.
        '''
        scheduling_list = Scheduling.objects.filter(workflow_uuid=workflow_uuid).values('uuid', 'workflow_uuid', 'scheduled_at', 'interval', 'is_active', 'created_at', 'updated_at')
        return list(scheduling_list.values())
    
    def get_scheduling_list(self):
        '''
        모든 Scheduling의 리스트를 반환한다.
        '''
        scheduling_list = Scheduling.objects.all()
        return list(scheduling_list.values())

    def update_scheduling(self, scheduling_uuid, scheduled_at, interval, repeat_count):
        '''
        일치하는 Scheduling을 인자에 주어진 정보로 수정한다.
        '''
        try:
            scheduling = Scheduling.objects.get(uuid=scheduling_uuid)
            
            scheduling.scheduled_at = parse_datetime(scheduled_at) if scheduled_at else scheduling.scheduled_at
            scheduling.interval = timedelta(**interval) if interval else scheduling.interval
            scheduling.repeat_count = repeat_count if repeat_count else scheduling.repeat_count

            scheduling.save()

            return scheduling
        except ObjectDoesNotExist:
            return {'status': 'error', 'message': 'Scheduling not found'}
        except MultipleObjectsReturned:
            return {'status': 'error', 'message': 'Multiple schedulings found with the same UUID'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def delete_scheduling(self, scheduling_uuid):
        '''
        일치하는 Scheduling 정보를 삭제한다.
        '''
        try:
            scheduling = Scheduling.objects.get(uuid=scheduling_uuid)
            scheduling.delete()
            return {'status': 'success', 'message': 'Scheduling deleted successfully'}
        except ObjectDoesNotExist:
            return {'status': 'error', 'message': 'Scheduling not found'}
        except MultipleObjectsReturned:
            return {'status': 'error', 'message': 'Multiple Schedulings found with the same UUID'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
