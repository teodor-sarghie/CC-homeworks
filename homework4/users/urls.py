from django.urls import path

from users.views import (
    RegisterView,
    CustomLoginView,
    CustomLogoutView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("users/<int:pk>", UserDetailView.as_view(), name="user-view"),
    path("users/<int:pk>/update", UserUpdateView.as_view(), name="user-update"),
    path("users/<int:pk>/delete", UserDeleteView.as_view(), name="user-delete"),
]
