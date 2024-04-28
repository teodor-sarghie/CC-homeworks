from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", )


class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label="New password", widget=forms.PasswordInput, required=False
    )
    password2 = forms.CharField(
        label="Confirm new password", widget=forms.PasswordInput, required=False
    )

    class Meta:
        model = User
        fields = ("email", )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Passwords don't match")
            try:
                password_validation.validate_password(password2)
            except ValidationError as error:
                self.add_error("password2", error)
        elif password1 and not password2:
            self.add_error("password2", "You have to fill this field !")
        elif not password1 and password2:
            self.add_error("password1", "You have to fill this field !")
        return password2


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", required=True)
