from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from project_apps.models import Workflow


class WorkflowRepository:
    def create_workflow(self, name, description):
        workflow = Workflow.objects.create(name=name, description=description)
        return workflow

    def get_workflow(self, workflow_uuid):
        try:
            workflow = Workflow.objects.get(uuid=workflow_uuid)
            return workflow
        except ObjectDoesNotExist:
            return {'status': 'error', 'message': 'Workflow not found'}
        except MultipleObjectsReturned:
            return {'status': 'error', 'message': 'Multiple workflows found with the same UUID'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def update_workflow(self, workflow_uuid, name, description):
        try:
            workflow = Workflow.objects.get(uuid=workflow_uuid)
            
            for arg, val in locals().items():
                if val is not None:
                    setattr(workflow, arg, val)
            workflow.save()

            return workflow
        except ObjectDoesNotExist:
            return {'status': 'error', 'message': 'Workflow not found'}
        except MultipleObjectsReturned:
            return {'status': 'error', 'message': 'Multiple workflows found with the same UUID'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def delete_workflow(self, workflow_uuid):
        try:
            workflow = Workflow.objects.get(uuid=workflow_uuid)
            workflow.delete()
            return {'status': 'success', 'message': 'Workflow deleted successfully'}
        except ObjectDoesNotExist:
            return {'status': 'error', 'message': 'Workflow not found'}
        except MultipleObjectsReturned:
            return {'status': 'error', 'message': 'Multiple workflows found with the same UUID'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_workflow_list(self):
        workflow_list = Workflow.objects.all()
        return workflow_list
