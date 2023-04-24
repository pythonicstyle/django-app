from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Profile, User
from .forms import UserUpdateForm


class AboutMeView(UpdateView):
    template_name = "myauth/about-me.html"
    model = Profile
    fields = ['avatar']

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse("myauth:about-me")


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


class UsersListView(ListView):
    model = User
    template_name = 'myauth/users_list.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    template_name = 'myauth/user_details.html'
    queryset = User.objects.all()


class UserUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.pk == self.get_object().pk \
            or self.request.user.is_staff

    model = Profile
    fields = ['bio', 'avatar']
    template_name = 'myauth/user_update_form.html'

    def get_success_url(self):
        return reverse("myauth:users_list")


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
