from django import forms
from forum_comments.models import Article, UserModel, Comment


class Login(forms.Form):
    username = forms.CharField(max_length= 30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)


class formArticle(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text']


class registerUserForm(forms.ModelForm):
    password1 = forms.CharField(max_length=150, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=150, widget=forms.PasswordInput)
    class Meta:
        model = UserModel
        fields = ['username', 'email']


class ResetPassUser(forms.Form):
    email = forms.CharField(max_length=150)


class ResetPassword(forms.Form):
    password = forms.CharField(max_length=150)
    password_repeat = forms.CharField(max_length=150)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class CreateUserAdmin(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    class Meta:
        model = UserModel
        fields = ['username', 'email']
