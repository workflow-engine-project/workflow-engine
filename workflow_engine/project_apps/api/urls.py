from django.urls import path

from project_apps.api.views import WorkflowAPIView, WorkflowListReadAPIView, WorkflowExecuteAPIView

urlpatterns = [
    path('workflow', WorkflowAPIView.as_view()),
    path('workflow/<uuid:workflow_uuid>', WorkflowAPIView.as_view()),
    path('workflow/list', WorkflowListReadAPIView.as_view()),
    path('workflow/execute/<uuid:workflow_uuid>', WorkflowExecuteAPIView.as_view()),
]
