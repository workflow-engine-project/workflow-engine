from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid

class Workflow(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Job(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    parameters = models.JSONField()
    next = ArrayField(models.UUIDField(), blank=True, null=True)
    depends_cnt = models.IntegerField()

class History(models.Model):
    id = models.AutoField(primary_key=True)
    workflow_id = models.UUIDField(default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20)
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField()

class Scheduling(models.Model):
    id = models.AutoField(primary_key=True)
    workflow_id = models.UUIDField(default=uuid.uuid4, editable=False)
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
