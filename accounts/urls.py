from django.contrib.auth import views as auth_views
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet

from . import views

router = DefaultRouter()
router.register(r"api/auth", AuthViewSet, basename="auth")

urlpatterns = [
    # web based views
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # path("signup/", views.signup_view, name="signup"),
    # path("home/", views.home_view, name="home"),
] + router.urls
