from project_apps.models import History

class HistoryRepository:
    def create_history(self, workflow_uuid, status, started_at, completed_at):
        pass

    def get_history(self, history_uuid):
        pass

    def delete_history(self, history_uuid):
        pass
