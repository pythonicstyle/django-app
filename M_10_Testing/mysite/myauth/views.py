from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, View

from .models import Profile


class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return response


class MyLoginView(LoginView):
    template_name = "myauth/login.html"
    redirect_authenticated_user = True


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("data", "some info", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("data", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["username"] = request.user.username
    return HttpResponse("Session set")


@login_required()
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("username", "no data yet")
    return HttpResponse(f"Session value, user: {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})
