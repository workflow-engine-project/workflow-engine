from django.db import models
import uuid


class Job(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow_uuid = models.UUIDField()
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    parameters = models.TextField()
    next_job_uuid = models.UUIDField(blank=True, null=True)
    depends_count = models.IntegerField()
