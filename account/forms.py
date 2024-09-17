from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        # widgets = {
        #     "username": TextInput(attrs={"class": "form-control"}),
        #     "email": TextInput(attrs={"class": "form-control"}),
        #     "password1": PasswordInput(attrs={"class": "form-control"}),
        #     "password2": PasswordInput(attrs={"class": "form-control"}),
        # }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.fields["email"].label = "Your Email Adress"
        self.fields["email"].required = True
        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists() or len(email) > 254:
            raise forms.ValidationError("Email already exists")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["email"].label = "Your Email Adress"

    class Meta:
        model = User
        fields = ["username", "email"]
        exclude = ("password1", "password2")
