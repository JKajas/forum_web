import secrets

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView

from forum_comments.forms import (
    CommentForm,
    LoginForm,
    NewPassword,
    ResetPassword,
    formArticle,
    registerUserForm,
)
from forum_comments.models import Article, Comment, PasswordToken, UserModel


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        login(self.request, form.user)
        return super().form_valid(form)


class IndexView(ListView):
    template_name = "index.html"
    paginate_by = 4
    queryset = Article.objects.all().order_by("-time")
    context_object_name = "article"

    def get_queryset(self):
        if not "title" in self.request.GET:
            return super().get_queryset()
        queryset = Article.objects.filter(
            title__regex=self.request.GET["title"]
        ).order_by("-date")
        return queryset


class SignUpView(FormView):
    template_name = "signup.html"
    form_class = registerUserForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        username = self.request.POST["username"]
        email = self.request.POST["email"]
        password = self.request.POST["password"]
        register_user = UserModel(username=username, email=email)
        register_user.set_password(password)
        register_user.save()
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class ProfileView(ListView):
    template_name = "profile.html"
    context_object_name = "users_article"

    def post(self, request, **kwargs):
        if self.request.headers.get("x-requested-with") != "XMLHttpRequest":
            return super().post(request)
        article_to_del = Article.objects.get(pk=self.request.POST["delete"])
        article_to_del.delete()

    def get_queryset(self):
        queryset = Article.objects.filter(author=self.request.user.id)
        return queryset


@method_decorator(login_required, name="dispatch")
class LogoutView(TemplateView):
    template_name = "logout.html"

    def get(self, request, **kwargs):
        logout(request)
        return self.render_to_response(self.get_context_data(**kwargs))


@method_decorator(login_required, name="dispatch")
class AddArticleView(FormView):
    form_class = formArticle
    template_name = "add_article.html"

    def get_success_url(self):
        return reverse(
            "add_article", kwargs={"username": self.request.user.username}
        )

    def form_valid(self, form):
        Article.objects.create(
            author=self.request.user,
            title=self.request.POST["title"],
            text=self.request.POST["text"],
            image=self.request.FILES["image"],
            url=secrets.token_urlsafe(10),
        )
        return super().form_valid(form)


class ResetPasswordFormView(FormView):
    form_class = ResetPassword
    template_name = "resetpassword.html"
    success_url = reverse_lazy("resetpassword")

    def form_valid(self, form):
        try:
            user = UserModel.objects.get(email=self.request.POST["email"])
            url_token = secrets.token_urlsafe(16)
            passwordtoken = PasswordToken(token=url_token, username=user)
            data_to_msg = {
                "user": user.username,
                "address": settings.ALLOWED_HOSTS[0],
                "token": url_token,
            }
            message = mail.EmailMessage(
                subject="test",
                body=render_to_string("email_template.html", data_to_msg),
                from_email="test@test.com",
                connection=mail.get_connection(),
                to=[f"{user.email}"],
            )
            message.content_subtype = "html"
            passwordtoken.save()
            message.send()
        except:
            pass
        return super().form_valid(form)


class NewPasswordView(FormView):
    template_name = "newpassword.html"
    form_class = NewPassword
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        password = self.request.POST["password"]
        username = UserModel.objects.get(
            passwordtoken__token=self.kwargs["url_token"]
        )

        username.set_password(password)
        username.save()
        return super().form_valid(form)


class ShowArticleView(FormView):
    template_name = "article.html"
    form_class = CommentForm

    def get_success_url(self):
        return reverse("article", kwargs={"url": self.kwargs["url"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["article"] = Article.objects.get(url=self.kwargs["url"])
        context["comments"] = Comment.objects.all().filter(
            article__url=self.kwargs["url"]
        )
        return context

    def post(self, request, **kwargs):
        if request.headers.get("x-requested-with") != "XMLHttpRequest":
            return super().post(request)
        com_to_del = Comment.objects.get(pk=self.request.POST["delete"])
        com_to_del.delete()

    def form_valid(self, form):
        Comment.objects.create(
            author=self.request.user,
            article=Article.objects.get(url=self.kwargs["url"]),
            text=self.request.POST["text"],
        )
        return super().form_valid(form)
