from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode

from . import models

"""
Middleware fixes problem with url with any user in database 
Example:
Url patern: /profile/<username> 
If url address is: localhost:8000/profile/exuser, but logged user has username: userexample
and exuser is in database you can reach that endpoint
Middleware changes argument <username> on correct logged username
"""


class CheckCompatibility:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.user.is_authenticated:
                if request.user.username != view_kwargs["username"]:
                    return redirect(
                        reverse(
                            view_func,
                            kwargs={"username": request.user.username},
                        )
                    )
        except:
            return None


# Middleware check if token is in database


class CheckToken:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if not models.PasswordToken.objects.filter(
                token=view_kwargs["url_token"]
            ).exists():
                return redirect("index")
            return None
        except:
            None


class SearchQuery:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if not request.GET["title"]:
                return None
            if not request.path == reverse("index"):
                return redirect(
                    reverse("index") + "?title=" + request.GET["title"]
                )
        except:
            None
