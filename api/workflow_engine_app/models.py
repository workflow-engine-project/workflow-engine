from django.db import models
import uuid

class Workflow(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Job(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow_uuid = models.UUIDField()
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    parameters = models.TextField()
    nextjob_uuid = models.CharField(max_length=255, blank=True, null=True)
    depends_count = models.IntegerField()

class History(models.Model):
    workflow_uuid = models.UUIDField()
    status = models.CharField(max_length=20)
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField()
