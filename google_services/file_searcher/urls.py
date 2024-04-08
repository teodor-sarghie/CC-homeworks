from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add_file/", views.add_file, name="add_file"),
]
