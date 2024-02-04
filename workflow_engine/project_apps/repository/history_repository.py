from project_apps.models import History

class HistoryRepository:
    def create_history(self, workflow_uuid):
        history = History.objects.create(workflow_uuid=workflow_uuid)
        return history

    def get_history(self, history_uuid):
        return History.objects.get(uuid=history_uuid)

    def delete_history(self, history_uuid):
        history = History.objects.get(uuid=history_uuid)
        history.delete()
