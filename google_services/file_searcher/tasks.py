import logging
from io import BytesIO

import pdfplumber
from django.core.files.storage import default_storage

from Drives.GoogleDrive import GoogleDrive
from google_services.celery import app

from users.models import User
from file_searcher.models import FileUpload, FileAnalyzer
from file_searcher.analyze import (
    save_temporary_file,
    classify_text,
    extract_sentiment,
    extract_text_from_pdf,
)
from django.utils import timezone


@app.task
def upload_file_to_google_drive(file_id, file_path, file_name, mime_type):
    file_up = FileUpload.objects.get(id=file_id)
    try:
        gd = GoogleDrive(file_up.user)
        gd.connect()

        with default_storage.open(file_path, "rb") as file_obj:
            file_id = gd.upload_file_directly(file_obj, file_name, mime_type=mime_type)

        default_storage.delete(file_path)
        file_up.google_drive_id = file_id
        file_up.upload_time = timezone.now()
        file_up.status = FileUpload.Status.SUCCESS
    except Exception as e:
        logging.error(f"ERROR WHILE UPLOADING FILE {e}")
        file_up.status = FileUpload.Status.FAILED
    finally:
        file_up.save()


@app.task
def delete_file_from_google_drive(file_id):
    file = FileUpload.objects.get(id=file_id)
    try:
        gd = GoogleDrive(file.user)
        gd.connect()
        gd.delete_file(file.google_drive_id)
    except Exception as e:
        logging.error(f"CE ERROR MEA {e}")
        if file.google_drive_id is None:
            file.delete()
        else:
            file.status = FileUpload.Status.FAILED_DELETION
            file.save()
    else:
        file.delete()


@app.task
def analyze_file(file_analysis_id):
    file_analyzer = FileAnalyzer.objects.select_related("file", "file__user").get(
        id=file_analysis_id
    )
    file_path = file_analyzer.file.file_path

    text = ""
    with default_storage.open(file_path, "rb") as file:
        pdf_bytes = file.read()

        pdf_bio = BytesIO(pdf_bytes)
        try:
            with pdfplumber.open(pdf_bio) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    text += page_text + "\n"
        except Exception as e:
            file_analyzer.error = "Possibly encrypted PDF or corrupted"
            file_analyzer.status = FileAnalyzer.Status.EXTRACT_TEXT_FAIL
            file_analyzer.save()
            return

    sentiment = None
    categories = None
    try:
        sentiment = extract_sentiment(text)
    except Exception as e:
        file_analyzer.status = FileAnalyzer.Status.PARTIAL_SUCCESS
        file_analyzer.error_analyzer = str(e)
        file_analyzer.save()
        logging.error(f"CE EROARE 4 {e}")
    else:
        file_analyzer.error_analyzer = None
        file_analyzer.save()

    try:
        categories = classify_text(text)
    except Exception as e:
        file_analyzer.status = FileAnalyzer.Status.FAILED
        file_analyzer.error_classifier = str(e)
        file_analyzer.save()
        logging.error(f"CE EROARE 5 {e}")
    else:
        file_analyzer.error_classifier = None
        file_analyzer.save()
        logging.error(f"categories {categories}")

    if sentiment is not None and categories is not None:
        file_analyzer.status = FileAnalyzer.Status.SUCCESS

    file_analyzer.sentiment = sentiment
    file_analyzer.categories = categories
    file_analyzer.save()
