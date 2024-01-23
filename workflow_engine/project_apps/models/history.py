from django.db import models
import uuid


class History(models.Model):
    STATUS_CHOICES = [
        ('running', 'running'),
        ('success', 'success'),
        ('fail', 'fail')
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow_uuid = models.UUIDField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='running')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)
