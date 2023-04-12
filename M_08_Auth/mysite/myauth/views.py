from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy


class MyLoginView(LoginView):
    template_name = "myauth/login.html"
    redirect_authenticated_user = True


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("data", "some info", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("data", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["username"] = request.user.username
    return HttpResponse("Session set")


def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("username", "no data yet")
    return HttpResponse(f"Session value, user: {value!r}")
