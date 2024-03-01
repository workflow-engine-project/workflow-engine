from datetime import timedelta

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.utils.dateparse import parse_datetime

from project_apps.models import Scheduling


class SchedulingRepository:
    def create_scheduling(self, workflow_uuid, scheduled_at, interval, repeat_count):
        parse_scheduled_at = parse_datetime(scheduled_at) if scheduled_at else None
        parse_interval = timedelta(**interval) if interval else None

        scheduling = Scheduling.objects.create(
            workflow_uuid=workflow_uuid, 
            scheduled_at=parse_scheduled_at, 
            interval=parse_interval, 
            repeat_count=repeat_count
        )
    
    def get_scheduling(self, scheduling_uuid):
        try:
            scheduling = Scheduling.objects.get(uuid=scheduling_uuid)
            return scheduling
        except ObjectDoesNotExist:
            return {'status': 'error', 'message': 'Scheduling not found'}
        except MultipleObjectsReturned:
            return {'status': 'error', 'message': 'Multiple schedulings found with the same UUID'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_scheduling_list(self, workflow_uuid):
        scheduling_list = Scheduling.objects.filter(workflow_uuid=workflow_uuid).values('uuid', 'workflow_uuid', 'scheduled_at', 'interval', 'is_active', 'created_at', 'updated_at')
        return list(scheduling_list.values())

    def update_scheduling(self, scheduling_uuid, scheduled_at, interval, repeat_count, is_active):
        try:
            scheduling = Scheduling.objects.get(uuid=scheduling_uuid)
            
            for arg, val in locals().items():
                if val is not None:
                    setattr(scheduling, arg, val)
            scheduling.save()

            return scheduling
        except ObjectDoesNotExist:
            return {'status': 'error', 'message': 'Scheduling not found'}
        except MultipleObjectsReturned:
            return {'status': 'error', 'message': 'Multiple schedulings found with the same UUID'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def delete_scheduling(self, scheduling_uuid):
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
