from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import FormView, DeleteView

from Drives.GoogleDrive import GoogleDrive
from file_searcher.forms import FileUploadForm
from file_searcher.models import FileUpload, FileAnalyzer
from file_searcher.tasks import (
    upload_file_to_google_drive,
    delete_file_from_google_drive,
    analyze_file,
)


class AddFileView(LoginRequiredMixin, FormView):
    template_name = "file_searcher/add_file.html"
    form_class = FileUploadForm
    success_url = reverse_lazy("add-file")

    def form_valid(self, form):
        uploaded_file = self.request.FILES.get("file")
        temp_file_path = default_storage.save(
            f"tmp/{uploaded_file.name}", ContentFile(uploaded_file.read())
        )
        file_up = FileUpload(
            file_name=uploaded_file.name,
            user=self.request.user,
            file_path=temp_file_path,
            status=FileUpload.Status.SUCCESS,
        )
        file_up.save()
        messages.success(self.request, "File uploaded.")
        return super().form_valid(form)


class FileUploadListView(LoginRequiredMixin, ListView):
    model = FileUpload
    template_name = "file_searcher/list.html"

    def get_queryset(self):
        return (
            FileUpload.objects.select_related("user")
            .filter(user=self.request.user)
            .order_by(F("upload_time").desc())
        )


class FileUploadDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "file_searcher/delete.html"
    model = FileUpload
    success_url = reverse_lazy("file-upload-list")

    def get_object(self, queryset=None):
        return get_object_or_404(
            FileUpload, pk=self.kwargs.get("pk"), user=self.request.user
        )

    def form_valid(self, form):
        self.object = self.get_object()
        default_storage.delete(self.object.file_path)
        self.object.delete()
        messages.info(self.request, "File deleted")
        return HttpResponseRedirect(self.get_success_url())


class FileAnalyzerListView(LoginRequiredMixin, ListView):
    model = FileAnalyzer
    template_name = "file_searcher/analyzer/list.html"

    def get_queryset(self):
        return (
            FileAnalyzer.objects.select_related("file")
            .filter(file__user=self.request.user, file__id=self.kwargs.get("pk"))
            .order_by(F("created_at").desc())
        )


class FileAnalyzerView(LoginRequiredMixin, TemplateView):

    def get(self, *args, **kwargs):
        file = get_object_or_404(FileUpload, id=self.kwargs.get("pk"))
        file_analyzer = FileAnalyzer(file=file)
        file_analyzer.save()

        analyze_file.delay(file_analyzer.id)
        messages.info(self.request, "File sent for analysis")
        return HttpResponseRedirect(reverse_lazy("file-upload-list"))


class RepeatFileAnalysisView(LoginRequiredMixin, TemplateView):

    def get(self, *args, **kwargs):
        file_analyzer = get_object_or_404(FileAnalyzer, id=self.kwargs.get("pk"))
        analyze_file.delay(file_analyzer.id)
        messages.info(self.request, "File sent for analysis")
        return HttpResponseRedirect(
            reverse_lazy("file-analyze-list", kwargs={"pk": file_analyzer.file.id})
        )


class FileAnalyzerDetailView(LoginRequiredMixin, DetailView):
    model = FileAnalyzer
    template_name = "file_searcher/analyzer/view.html"

    def get_object(self, queryset=None):
        return get_object_or_404(FileAnalyzer, id=self.kwargs.get("pk"))


class FileAnalyzerDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "file_searcher/analyzer/delete.html"
    model = FileAnalyzer

    def get_object(self, queryset=None):
        return get_object_or_404(
            FileAnalyzer, pk=self.kwargs.get("pk"), file__user=self.request.user
        )

    def form_valid(self, form):
        success_url = reverse_lazy(
            "file-analyze-list", kwargs={"pk": self.object.file.id}
        )
        self.object.delete()
        return HttpResponseRedirect(success_url)
