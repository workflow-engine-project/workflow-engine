from django.db import models
import uuid


class History(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow_uuid = models.UUIDField()
    status = models.CharField(max_length=20)
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField()
