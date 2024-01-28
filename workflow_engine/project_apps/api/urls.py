from django.urls import path

from project_apps.api.views import WorkflowCreateAPIView, WorkflowDeleteAPIView

urlpatterns = [
    path('workflow', WorkflowCreateAPIView.as_view()),
    path('workflow/delete/<uuid:workflow_uuid>/', WorkflowDeleteAPIView.as_view()),
]
