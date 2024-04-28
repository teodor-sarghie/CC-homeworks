from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView

from users.forms import CustomUserCreationForm, CustomAuthenticationForm, UserUpdateForm


User = get_user_model()


class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("home-page")


class CustomLogoutView(LoginRequiredMixin, LogoutView):

    def get_success_url(self):
        return reverse_lazy("login")


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/view.html"

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "users/update.html"
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_success_url(self):
        return reverse_lazy("user-view", kwargs={"pk": self.request.user.pk})


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("login")
    template_name = "users/delete.html"

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)
