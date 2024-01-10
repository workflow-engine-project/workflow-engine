from django.db import models
import uuid
from .workflow import Workflow

class Job(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow_uuid = models.UUIDField()
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    parameters = models.TextField()
    nextjob_uuid = models.CharField(max_length=255, blank=True, null=True)
    depends_count = models.IntegerField()

    def get_workflow(self):
        try:
            return Workflow.objects.get(uuid=self.workflow_uuid)
        except Workflow.DoesNotExist:
            return None
