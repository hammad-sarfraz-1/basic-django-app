import re

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.response import Response
# DRF imports
from rest_framework.views import APIView

from .forms import LoginForm, SignUpForm


# -------------------------------------
# DRF Login API with Validation
# -------------------------------------
class LoginAPI(APIView):
    def post(self, request):
        username = request.data.get("username", "").strip()
        password = request.data.get("password", "").strip()

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response(
                {"message": "Logged in successfully"}, status=status.HTTP_200_OK
            )
        return Response(
            {"error": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


# -------------------------------------
# DRF Signup API with Validation
# -------------------------------------
class SignupAPI(APIView):
    def post(self, request):
        username = request.data.get("username", "").strip()
        password = request.data.get("password", "").strip()
        email = request.data.get("email", "").strip()

        # Required fields check
        if not username or not password or not email:
            return Response(
                {"error": "Username, password, and email are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Username length
        if len(username) < 4:
            return Response(
                {"error": "Username must be at least 4 characters long."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Password strength
        if len(password) < 6:
            return Response(
                {"error": "Password must be at least 6 characters long."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return Response(
                {"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Uniqueness checks
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Create user
        try:
            User.objects.create_user(username=username, password=password, email=email)
            return Response(
                {"message": "User created successfully"}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": f"User creation failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# -------------------------------------
# Traditional Django Views
# -------------------------------------
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            pwd = form.cleaned_data["password1"]
            user = authenticate(username=username, password=pwd)
            login(request, user)
            return redirect("home")  # make sure 'home' is named in your URLs
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    django_logout(request)
    return redirect("login")  # make sure 'login' is named in your URLs


@login_required
def home_view(request):
    return render(request, "home.html", {"user": request.user})
