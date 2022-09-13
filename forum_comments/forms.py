from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from forum_comments import validators

from forum_comments.models import Article, Comment, UserModel


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        label="Email address",
        widget=forms.TextInput(attrs={"placeholder": "email@example.com"}),
    )
    password = forms.CharField(
        max_length=30,
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )
    user = None
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        user = authenticate(
        email=username,
        password=password,
        )
        if user is None:
            raise ValidationError("Data is not correct. Check your email and password")
        self.user = user

class formArticle(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "text", "image"]
        labels = {"text": "", "title": "Title:"}
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Enter your article's title"}
            )
        }


class registerUserForm(forms.ModelForm):
    password = forms.CharField(
        max_length=150,
        label="Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password"}
        ),
    )
    password_repeat = forms.CharField(
        max_length=150,
        label="Repeat Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Repeat your password"}
        ),
    )

    class Meta:
        model = UserModel
        fields = ["username", "email"]
        labels = {"username": "Username", "email": "Email"}
        widgets = {
            "username": forms.TextInput(
                attrs={"placeholder": "Enter your username"}
            ),
            "email": forms.TextInput(
                attrs={"placeholder": "Enter your email"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")
        if password != password_repeat:
           raise ValidationError("Passwords should be the same!")
        validators.password_validator(password)


class ResetPassword(forms.Form):
    email = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Enter your email"}),
    )


class NewPassword(forms.Form):
    password = forms.CharField(
        max_length=150,
        label="New password",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your new password here"}
        ),
    )
    password_repeat = forms.CharField(
        max_length=150,
        label="Repeat new password",
        widget=forms.TextInput(
            attrs={"placeholder": "Repeat your new password"}
        ),
    )
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")
        if password != password_repeat:
            raise ValidationError("Passwords should be the same", code="invalid")
        with open(settings.BASE_DIR / "leaked_passwords.txt","r") as leaked_password:
            if password in leaked_password.read():
                raise ValidationError("Your password is too popular")
        validators.password_validator(password)

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs.update(
            {"placeholder": "Write your comment here"}
        )

    class Meta:
        model = Comment
        fields = ["text"]


class CreateUserAdmin(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ["username", "email"]
