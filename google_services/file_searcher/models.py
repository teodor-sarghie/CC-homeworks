from django.db import models
from django.utils import timezone
from users.models import User


class FileUpload(models.Model):
    class Status(models.TextChoices):
        PROCESSING = "processing"
        FAILED = "failed"
        SUCCESS = "success"
        FAILED_DELETION = "failed_deletion"

    file_name = models.CharField(max_length=256)
    google_drive_id = models.CharField(max_length=64, blank=True, null=True)
    upload_time = models.DateTimeField(default=timezone.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    status = models.CharField(
        choices=Status.choices, default=Status.PROCESSING, max_length=30
    )

    objects = models.Manager()

    def __str__(self):
        return self.file_name


class FileAnalyzer(models.Model):
    class Status(models.TextChoices):
        PROCESSING = "processing"
        FAILED = "failed"
        SUCCESS = "success"
        PARTIAL_SUCCESS = "partial_success"
        DOWNLOAD_FAIL = "download_file_failed"
        SAVE_LOCAL_FILE_FAIL = "save_local_file_failed"
        EXTRACT_TEXT_FAIL = "extract_text_failed"

    file = models.ForeignKey(
        FileUpload, on_delete=models.CASCADE, related_name="file_upload"
    )
    error_analyzer = models.CharField(max_length=1024, blank=True, null=True)
    error_classifier = models.CharField(max_length=1024, blank=True, null=True)
    sentiment = models.CharField(max_length=2048, blank=True, null=True)
    categories = models.CharField(max_length=2048, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now())
    error = models.CharField(max_length=1024, blank=True, null=True)
    status = models.CharField(
        choices=Status.choices, default=Status.PROCESSING, max_length=30
    )

    objects = models.Manager()
