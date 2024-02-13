from django.utils import timezone

from project_apps.constants import HISTORY_STATUS_SUCCESS
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
        
    def update_history_status(self, history_uuid, status):
        '''
        워크플로우가 성공적으로 종료 될 경우 또는 실패 할 경우 워크플로우의 실행 이력(history) 상태를 업데이트.
        '''
        completed_at = timezone.now()
        History.objects.filter(uuid=history_uuid).update(status=status, completed_at=completed_at)
