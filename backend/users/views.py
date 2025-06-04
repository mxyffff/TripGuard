from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import User

# Create your views here.

def home_view(request):
    return render(request, "users/home.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "올바른 이메일 형식이 아닙니다. 다시 입력해 주세요.")
        else:
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("user:home")
            else:
                messages.error(request, "이메일 또는 비밀번호가 잘못되었습니다. 다시 입력해 주세요.")

    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect("user:login")

def signup_view(request):
    if request.method == "GET":
        request.session['email_checked'] = False
        request.session['password_checked'] = False
        return render(request, "users/signup.html")

    email = request.POST.get("email")
    password = request.POST.get("password")
    password2 = request.POST.get("password2")
    name = request.POST.get("name")
    nickname = request.POST.get("nickname")
    action = request.POST.get("action")

    context = {
        "email": email,
        "password": password,
        "password2": password2,
        "name": name,
        "nickname": nickname,
    }

    def is_valid_email(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    if action == "check_email":
        if not email:
            messages.error(request, "이메일을 입력해 주세요.")
            request.session['email_checked'] = False
        elif not is_valid_email(email):
            messages.error(request, "올바른 이메일 형식이 아닙니다.")
            request.session['email_checked'] = False
        elif User.objects.filter(email=email).exists():
            messages.error(request, "이미 사용 중인 이메일입니다.")
            request.session['email_checked'] = False
        else:
            messages.success(request, "사용 가능한 이메일입니다.")
            request.session['email_checked'] = True
        return render(request, "users/signup.html", context)

    elif action == "check_password":
        if not password:
            messages.error(request, "비밀번호를 입력해 주세요.")
            request.session['password_checked'] = False
        elif password != password2:
            messages.error(request, "비밀번호가 일치하지 않습니다.")
            request.session['password_checked'] = False
        else:
            messages.success(request, "비밀번호가 일치합니다.")
            request.session['password_checked'] = True
        return render(request, "users/signup.html", context)

    elif action == "signup":
        email_checked = request.session.get('email_checked', False)
        password_checked = request.session.get('password_checked', False)

        if not email_checked:
            messages.error(request, "이메일 중복 확인을 해 주세요.")
            return render(request, "users/signup.html", context)

        if not password_checked:
            messages.error(request, "비밀번호 일치 확인을 해 주세요.")
            return render(request, "users/signup.html", context)

        if not all([email, password, password2, name, nickname]):
            messages.error(request, "모든 항목을 입력해 주세요.")
            return render(request, "users/signup.html", context)

        if not is_valid_email(email):
            messages.error(request, "올바른 이메일 형식이 아닙니다.")
            return render(request, "users/signup.html", context)

        if len(password) < 8:
            messages.error(request, "비밀번호는 8자 이상이어야 합니다.")
            return render(request, "users/signup.html", context)

        if len(name) < 2:
            messages.error(request, "이름은 2자 이상이어야 합니다.")
            return render(request, "users/signup.html", context)

        if len(nickname) < 1:
            messages.error(request, "닉네임은 1자 이상이어야 합니다.")
            return render(request, "users/signup.html", context)

        User.objects.create_user(email=email, password=password, name=name, nickname=nickname)

        request.session['email_checked'] = False
        request.session['password_checked'] = False

        return redirect("user:login")

    else:
        messages.error(request, "잘못된 요청입니다.")
        return render(request, "users/signup.html", context)