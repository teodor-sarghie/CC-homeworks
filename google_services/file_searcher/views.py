from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from file_searcher.forms import FileUploadForm
from file_searcher.tasks import upload_file_to_google_drive
from Drives.GoogleDrive import GoogleDrive


def home(request):
    return render(request, "index.html")


class AddFileView(LoginRequiredMixin, FormView):
    template_name = "file_searcher/add_file.html"
    form_class = FileUploadForm
    success_url = reverse_lazy("add-file")

    def form_valid(self, form):
        uploaded_file = self.request.FILES.get("file")
        if uploaded_file:
            temp_file_path = default_storage.save(f"tmp/{uploaded_file.name}", ContentFile(uploaded_file.read()))

            upload_file_to_google_drive.delay(
                self.request.user.email,
                temp_file_path,
                uploaded_file.name,
                uploaded_file.content_type
            )

        return super().form_valid(form)
