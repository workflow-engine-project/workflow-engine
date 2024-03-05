from django.utils import timezone

from project_apps.constants import HISTORY_STATUS_SUCCESS
from project_apps.models import History


class HistoryRepository:
    '''
    History 정보를 관리하는 리포지토리.
    '''
    def create_history(self, workflow_uuid):
        '''
        History 정보를 생성한다.
        '''
        history = History.objects.create(workflow_uuid=workflow_uuid)
        return history

    def get_history(self, history_uuid):
        '''
        일치하는 History 정보를 반환한다.
        '''
        return History.objects.get(uuid=history_uuid)

    def delete_history(self, history_uuid):
        '''
        일치하는 History 정보를 삭제한다.
        '''
        history = History.objects.get(uuid=history_uuid)
        history.delete()
        
    def update_history_status(self, history_uuid, status):
        '''
        워크플로우가 성공적으로 종료되거나 실패할 경우 워크플로우의 실행 History 상태를 업데이트한다.
        '''
        completed_at = timezone.now()
        History.objects.filter(uuid=history_uuid).update(status=status, completed_at=completed_at)
