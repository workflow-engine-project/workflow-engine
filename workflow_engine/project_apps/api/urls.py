from django.urls import path

from project_apps.api.views import WorkflowCreateAPIView

urlpatterns = [
    path('workflow', WorkflowCreateAPIView.as_view()),
]
