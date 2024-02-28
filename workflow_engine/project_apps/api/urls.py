from django.urls import path

from project_apps.api.views import WorkflowAPIView, WorkflowListReadAPIView, WorkflowExecuteAPIView, SchedulingAPIView, SchedulingListReadAPIView

urlpatterns = [
    path('workflow', WorkflowAPIView.as_view()),
    path('workflow/<uuid:workflow_uuid>', WorkflowAPIView.as_view()),
    path('workflow/list', WorkflowListReadAPIView.as_view()),
    path('workflow/execute/<uuid:workflow_uuid>', WorkflowExecuteAPIView.as_view()),
    path('workflow/scheduling', SchedulingAPIView.as_view()),
    path('workflow/scheduling/<uuid:scheduling_uuid>', SchedulingAPIView.as_view()),
    path('workflow/scheduling/list/<uuid:workflow_uuid>', SchedulingListReadAPIView.as_view()),
]
