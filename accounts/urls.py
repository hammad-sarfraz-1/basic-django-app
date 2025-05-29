# accounts/urls.py

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("home/", views.home_view, name="home"),
    path(
        "api/login/", views.LoginAPI.as_view(), name="login_api"
    ),  # DRF login API if using class-based view
    path("api/signup/", views.SignupAPI.as_view(), name="api-signup"),
    # path('admin/', admin.site.urls)
]
