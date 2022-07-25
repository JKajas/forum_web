from django.shortcuts import render, redirect
from forum_comments.forms import Login, ResetPassword, formArticle, registerUserForm, ResetPassword, ResetPassUser, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from forum_comments.models import UserModel, Article, PasswordToken, Comment
import secrets
from django.core import mail
from django.conf import settings


def login_func(request):
        form = Login(request.POST)
        if form.is_valid():
            form.cleaned_data
            usernames = request.POST["username"]
            passwords = request.POST["password"]    
            user = authenticate(request, email=usernames, password=passwords)
            if user is not None:
               return login(request, user)


def index(request):
        articles = Article.objects.all()
        context = {
            "article" : articles,
            'form':Login
            }
        if request.method == "POST":
            login_func(request)
            return render(request, 'index.html', context)
        return render(request, 'index.html', context)


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1==password2:
            register_user = UserModel(username=username, email=email)
            register_user.set_password(password1)
            register_user.save()

    return render(request, "signup.html", {"form3":registerUserForm})


@login_required
def profile(request, username=None):
 
        users_article = Article.objects.filter(author=request.user.id)
        return render(request,'profile.html',{'users_article':users_article}) 
        ##dodać usuwanie artykułu


@login_required
def exit(request):
    logout(request)
    return render(request, "logout.html")


@login_required
def add_article(request, username=None):
        if request.method =='POST':
            title = request.POST['title']
            text = request.POST['text']
            author = request.user
            urls = secrets.token_urlsafe(10)
            form2 = formArticle(request.POST)
            if form2.is_valid():
                form2.cleaned_data
                article = Article(title=title,text=text,author=author, url=urls)
                article.save()
                render(request, "add_article.html", {"form2": formArticle})
        return render(request, "add_article.html", {"form2": formArticle})


def resetpassworduser(request):
    if request.method == "POST":
        form = ResetPassUser(request.POST)
        if form.is_valid():
            form.cleaned_data
            try:
                user = UserModel.objects.get(email=request.POST['email'])
                if user:
                    with mail.get_connection() as connection:
                        url_token = secrets.token_urlsafe(16)
                        passwordtoken = PasswordToken(token=url_token, username=user)
                        message = mail.EmailMessage(
                            body = f"Hey {user.username}, <p> If you'd like to reset your password click this link:<a href='http://{settings.ALLOWED_HOSTS[0]}:8000/resetpassword/{url_token}'>http://{settings.ALLOWED_HOSTS[0]}:8000/resetpassword/{url_token}</a>",
                            connection = connection, 
                            to=[f"{user.email}"])
                        message.content_subtype = "html"
                        passwordtoken.save()
                        message.send()
            except:
                redirect('resetpassword')
    return render (request,"resetpassword.html", {"form":ResetPassUser})


def resetpassword(request,url_token):
    if request.method == "POST":
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']
        username = UserModel.objects.get(passwordtoken__token=url_token)
        if password == password_repeat:
           username.set_password(password)
           username.save()
           return redirect('index')
    return render(request, "resetpass.html", {'form':ResetPassword})


def show_article(request, url):
    article = Article.objects.get(url=url)
    comments = Comment.objects.all().filter(article__url = url)
    context = {
        "article" : article,
        "comment_form" : CommentForm,
        "comments" : comments
    }
    if request.method == "POST":
        '''
        If request is ajax
        '''
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            com_to_del = Comment.objects.get(pk= request.POST['delete'])
            com_to_del.delete()
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                form.cleaned_data
                comment = Comment(author = request.user, article= article, text= request.POST["text"])
                comment.save()
    return render(request, 'article.html', context)
