from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Create your views here.

def login_view(request):
    error_message = ""

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(username = email, password = password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = "이메일 또는 비밀번호를 확인해 주세요."

    return render(request, "users/login.html", {
        "error_message": error_message,
    })