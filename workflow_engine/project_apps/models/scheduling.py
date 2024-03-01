from django.db import models
import uuid


class Scheduling(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow_uuid = models.UUIDField()
    scheduled_at = models.DateTimeField(null=True)
    interval = models.DurationField(null=True)
    repeat_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
