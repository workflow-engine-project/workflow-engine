from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from project_apps.models import Scheduling


class SchedulingRepository:
    def create_scheduling(self, workflow_uuid, scheduled_at, interval, is_active):
        scheduling = Scheduling.objects.create(workflow_uuid=workflow_uuid, scheduled_at=scheduled_at, interval=interval, is_active=is_active)
        return scheduling

    def update_scheduling(self, scheduling_uuid, scheduled_at, interval, is_active):
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
