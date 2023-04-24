from django.urls import path

from .views import (
    MyLoginView,
    MyLogoutView,
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view,
    AboutMeView,
    RegisterView,
    UserDetailView,
    UserUpdateView,
    UsersListView,
    FooBarView,
)

app_name = "myauth"

urlpatterns = [
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("register/", RegisterView.as_view(), name="register"),
    path("users/", UsersListView.as_view(), name="users_list"),
    path("users/<int:pk>/user-details/", UserDetailView.as_view(), name="user-details"),
    path("users/<int:pk>/update-user/", UserUpdateView.as_view(), name="user-update"),

    path("cookie/get/", get_cookie_view, name="cookie_get"),
    path("cookie/set/", set_cookie_view, name="cookie_set"),

    path("session/get/", get_session_view, name="session_get"),
    path("session/set/", set_session_view, name="session_set"),

    path("foo-bar/", FooBarView.as_view(), name="foo-bar"),
]
