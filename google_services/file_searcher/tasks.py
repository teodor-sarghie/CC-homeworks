from django.core.files.storage import default_storage

from Drives.GoogleDrive import GoogleDrive
from google_services.celery import app

from users.models import User
from file_searcher.models import FileUpload
from django.utils import timezone


@app.task
def upload_file_to_google_drive(user_email, file_path, file_name, mime_type):
    user = User.objects.get(email=user_email)
    file_up = FileUpload(file_name=file_name, user=user)
    file_up.save()

    try:
        gd = GoogleDrive(user)
        gd.connect()

        with default_storage.open(file_path, 'rb') as file_obj:
            file_id = gd.upload_file_directly(file_obj, file_name, mime_type=mime_type)

        print(file_id, "FILE")

        default_storage.delete(file_path)
        file_up.google_drive_id = file_id
        file_up.upload_time = timezone.now()
        file_up.status = FileUpload.Status.SUCCESS
    except Exception:
        file_up.status = FileUpload.Status.FAILED
    finally:
        file_up.save()
