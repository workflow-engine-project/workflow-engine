from django.db import models
from .workflow import Workflow

class History(models.Model):
    workflow_uuid = models.UUIDField()
    status = models.CharField(max_length=20)
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField()

    def get_workflow(self):
        try:
            return Workflow.objects.get(uuid=self.workflow_uuid)
        except Workflow.DoesNotExist:
            return None
