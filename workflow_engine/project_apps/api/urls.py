from django.urls import path

from project_apps.api.views import WorkflowCreateAPIView, WorkflowReadAPIView, WorkflowListReadAPIView, WorkflowUpdateAPIView, WorkflowDeleteAPIView, WorkflowExecuteAPIView

urlpatterns = [
    path('workflow', WorkflowCreateAPIView.as_view()),
    path('workflow/<uuid:workflow_uuid>', WorkflowReadAPIView.as_view()),
    path('workflow/<uuid:workflow_uuid>', WorkflowUpdateAPIView.as_view()),
    path('workflow/<uuid:workflow_uuid>', WorkflowDeleteAPIView.as_view()),
    path('workflow/list', WorkflowListReadAPIView.as_view()),
    path('workflow/execute/<uuid:workflow_uuid>', WorkflowExecuteAPIView.as_view()),
]
