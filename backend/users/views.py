from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User

# Create your views here.

def login_view(request):
    error_message = ""

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
        else:
            error_message = "이메일 또는 비밀번호를 확인해 주세요."

    return render(request, "users/login.html", {
        "error_message": error_message,
    })

def logout_view(request):
    logout(request)
    return redirect("user:login")

def signup_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        User.objects.create_user(email=email, password=password)
        return redirect("user:login")

    return render(request, "users/signup.html")