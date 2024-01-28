from project_apps.models import Workflow

class WorkflowRepository:
    def create_workflow(self, name, description):
        workflow = Workflow.objects.create(name=name, description=description)
        return workflow

    def get_workflow(self, workflow_uuid):
        workflow = Workflow.objects.get(uuid=workflow_uuid)
        return workflow

    def update_workflow(self, workflow_uuid, **kwargs):
        # TODO: 업데이트 필드 확정
        # TODO: 확정된 필드를 매개변수로 전부 넣어주고 default 값을 None으로 설정하여 모든 필드 값을 받도록 설정
        pass

    def delete_workflow(self, workflow_uuid):
        Workflow.objects.get(uuid=workflow_uuid).delete()
