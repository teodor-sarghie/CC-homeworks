import os.path
import io
from django.conf import settings

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload


SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]


class GoogleDrive:
    def __init__(self, user):
        self.user = user
        self.creds = None

    def connect(self):

        if self.user.token:
            self.creds = Credentials.from_authorized_user_info(
                eval(self.user.token), SCOPES
            )

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(settings.BASE_DIR, "Drives/credentials.json"), SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            self.user.token = self.creds.to_json()
            self.user.expiration_time = self.creds.expiry
            self.user.save()

    def get_all_files(self):
        files_dict = {}

        try:
            service = build("drive", "v3", credentials=self.creds)

            results = (
                service.files()
                .list(pageSize=1000, fields="nextPageToken, files(id, name)")
                .execute()
            )
            items = results.get("files", [])
            if not items:
                files_dict["errorName"] = "No files inside your Drive"
            else:
                for item in items:
                    files_dict[item["name"]] = item["id"]

            while "nextPageToken" in results:
                page_token = results["nextPageToken"]
                results = (
                    service.files()
                    .list(
                        pageSize=1000,
                        fields="nextPageToken, files(id, name)",
                        pageToken=page_token,
                    )
                    .execute()
                )
                items = results.get("files", [])
                for item in items:
                    files_dict[item["name"]] = item["id"]

        except HttpError as error:
            print(f"An error occurred: {error}")

        return files_dict

    def get_service(self):
        return build("drive", "v3", credentials=self.creds)

    def download_file(self, file_id):
        service = self.get_service()

        file_metadata = service.files().get(fileId=file_id, fields="mimeType").execute()

        def file_stream():

            google_docs_export_map = {
                "application/vnd.google-apps.document": "application/pdf",
                "application/vnd.google-apps.spreadsheet": "application/pdf",
                "application/vnd.google-apps.presentation": "application/pdf",
            }

            if file_metadata["mimeType"] in google_docs_export_map:
                export_mime_type = google_docs_export_map[file_metadata["mimeType"]]
                request = service.files().export_media(
                    fileId=file_id, mimeType=export_mime_type
                )
            else:
                request = service.files().get_media(fileId=file_id)

            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request, chunksize=1228800)
            done = False
            while not done:
                _, done = downloader.next_chunk()
                fh.seek(0)
                yield fh.read()
                fh.truncate(0)
                fh.seek(0)

        return file_stream

    def export_file_as_pdf(self, file_id):
        service = self.get_service()

        export_mime_type = "application/pdf"

        request = service.files().export_media(
            fileId=file_id, mimeType=export_mime_type
        )

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
        done = False
        while not done:
            _, done = downloader.next_chunk()
            fh.seek(0)
            yield fh.read()
            fh.truncate(0)
            fh.seek(0)

    def upload_file_directly(
        self, file_obj, file_name, mime_type="application/octet-stream"
    ):
        service = self.get_service()

        file_metadata = {"name": file_name}
        media = MediaIoBaseUpload(file_obj, mimetype=mime_type, resumable=True)
        try:
            file = (
                service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )
            print(f"Uploaded file ID: {file.get('id')}")
            return file.get("id")
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def delete_file(self, file_id):
        service = self.get_service()

        try:
            service.files().delete(fileId=file_id).execute()
            print(f"File with ID {file_id} has been deleted successfully.")
            return True
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
