from django.urls import path

from project_apps.api.views import *

urlpatterns = [
    path('workflow', WorkflowAPIView.as_view()),
    path('workflow/<uuid:workflow_uuid>', WorkflowUUIDAPIView.as_view()),
    path('workflow/<uuid:workflow_uuid>/execute', WorkflowExecuteAPIView.as_view()),
    path('scheduling', SchedulingAPIView.as_view()),
    path('scheduling/<uuid:scheduling_uuid>', SchedulingUUIDAPIView.as_view()),
    path('scheduling/workflow/<uuid:workflow_uuid>', SchedulingWorkflowAPIView.as_view()),
    path('scheduling/<uuid:scheduling_uuid>/execute', SchedulingExecuteAPIView.as_view()),
    path('scheduling/<uuid:scheduling_uuid>/deactive', SchedulingDeactivateAPIView.as_view()),
]
