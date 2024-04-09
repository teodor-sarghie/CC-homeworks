from django.urls import path
from file_searcher.views import (
    AddFileView,
    FileUploadListView,
    FileUploadDeleteView,
    FileAnalyzerListView,
    FileAnalyzerView,
    FileAnalyzerDetailView,
    FileAnalyzerDeleteView,
    RepeatFileAnalysisView,
)

urlpatterns = [
    path("add_file/", AddFileView.as_view(), name="add-file"),
    path("list/", FileUploadListView.as_view(), name="file-upload-list"),
    path("delete/<int:pk>", FileUploadDeleteView.as_view(), name="file-upload-delete"),
    path("analyze/<int:pk>", FileAnalyzerView.as_view(), name="file-analyze"),
    path(
        "analyze/<int:pk>/repeat",
        RepeatFileAnalysisView.as_view(),
        name="file-analyze-repeat",
    ),
    path(
        "analyze/<int:pk>/list",
        FileAnalyzerListView.as_view(),
        name="file-analyze-list",
    ),
    path(
        "analyze/<int:pk>/view",
        FileAnalyzerDetailView.as_view(),
        name="file-analyzer-view",
    ),
    path(
        "analyze/<int:pk>/delete",
        FileAnalyzerDeleteView.as_view(),
        name="file-analyzer-delete",
    ),
]
