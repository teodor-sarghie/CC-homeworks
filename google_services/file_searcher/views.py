from Drives.GoogleDrive import GoogleDrive
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.urls import reverse_lazy
from file_searcher.forms import FileUploadForm


def home(request):
    return render(request, "index.html")


class AddFileView(FormView):
    template_name = "file_searcher/add_file.html"
    form_class = FileUploadForm
    success_url = reverse_lazy("add-file")

    def form_valid(self, form):
        uploaded_file = self.request.FILES.get("file")
        if uploaded_file:
            gd = GoogleDrive()
            gd.connect()
            file_id = gd.upload_file_directly(
                uploaded_file, uploaded_file.name, mime_type=uploaded_file.content_type
            )
            self.request.session["file_upload_msg"] = file_id
            print(file_id, "FILE")
        return super().form_valid(form)
