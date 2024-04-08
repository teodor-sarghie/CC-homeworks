from django.db import models
from django.utils import timezone
from users.models import User


class FileUpload(models.Model):
    class Status(models.TextChoices):
        PROCESSING = "processing"
        FAILED = "failed"
        SUCCESS = "success"

    file_name = models.CharField(max_length=256)
    google_drive_id = models.CharField(max_length=64, blank=True, null=True)
    upload_time = models.DateTimeField(default=timezone.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    status = models.CharField(choices=Status.choices, default=Status.PROCESSING, max_length=30)
