from django.urls import path
from file_searcher.views import home, AddFileView

urlpatterns = [
    path("", home, name="home-page"),
    path("add_file/", AddFileView.as_view(), name="add-file"),
]
