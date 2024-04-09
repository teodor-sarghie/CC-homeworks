from django.urls import path
from file_searcher.views import (
    home,
    AddFileView,
    FileUploadListView,
    FileUploadDeleteView,
    FileAnalyzerListView,
    FileAnalyzerView,
)

urlpatterns = [
    path("", home, name="home-page"),
    path("add_file/", AddFileView.as_view(), name="add-file"),
    path("list/", FileUploadListView.as_view(), name="file-upload-list"),
    path("delete/<int:pk>", FileUploadDeleteView.as_view(), name="file-upload-delete"),
    path("analyze/<int:pk>", FileAnalyzerView.as_view(), name="file-analyze"),
    path(
        "analyze/<int:pk>/list",
        FileAnalyzerListView.as_view(),
        name="file-analyze-list",
    ),
]
