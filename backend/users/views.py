from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from .models import User
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def home_api_view(request):
    if request.user.is_authenticated:
        user_data = {
            "email": request.user.email,
            "name": request.user.name,
            "nickname": request.user.nickname,
        }
    else:
        user_data = None

    return JsonResponse({
        "is_authenticated": request.user.is_authenticated,
        "user": user_data,
    })

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            return render(request, "login.html", {"error_message": "이메일과 비밀번호를 모두 입력해 주세요."})

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # 로그인 성공 시 홈으로 이동
        else:
            return render(request, "login.html", {"error_message": "이메일 또는 비밀번호가 잘못되었습니다."})

    # GET 요청일 때
    return render(request, "login.html")

@csrf_exempt
@require_http_methods(["POST"])
def login_api_view(request):
    email = request.POST.get("email")
    password = request.POST.get("password")

    if not email or not password:
        return JsonResponse({"success": False, "message": "이메일과 비밀번호를 모두 입력해 주세요."}, status=400)

    if not is_valid_email(email):
        return JsonResponse({"success": False, "message": "올바른 이메일 형식이 아닙니다. 다시 입력해 주세요."}, status=400)

    user = authenticate(username=email, password=password)

    if user:
        login(request, user)
        request.session.modified = True
        return JsonResponse({
            "success": True,
            "message": "로그인에 성공했습니다.",
            "user": {
                "email": user.email,
                "name": user.name,
                "nickname": user.nickname,
            }
        })
    else:
        return JsonResponse({"success": False, "message": "이메일 또는 비밀번호가 잘못되었습니다. 다시 입력해 주세요."}, status=401)

@csrf_exempt
@require_http_methods(["POST"])
def logout_api_view(request):
    logout(request)
    return JsonResponse({"success": True, "message": "로그아웃 되었습니다."})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def signup_api_view(request):
    if request.method == "GET":
        request.session['email_checked'] = False
        request.session['password_checked'] = False
        return JsonResponse({"message": "세션을 초기화했습니다."})

    email = request.POST.get("email")
    password = request.POST.get("password")
    password2 = request.POST.get("password2")
    name = request.POST.get("name")
    nickname = request.POST.get("nickname")
    action = request.POST.get("action")

    if action == "check_email":
        if not email:
            request.session['email_checked'] = False
            return JsonResponse({"success": False, "message": "이메일을 입력해 주세요."}, status=400)
        elif not is_valid_email(email):
            request.session['email_checked'] = False
            return JsonResponse({"success": False, "message": "올바른 이메일 형식이 아닙니다."}, status=400)
        elif User.objects.filter(email=email).exists():
            request.session['email_checked'] = False
            return JsonResponse({"success": False, "message": "이미 사용 중인 이메일입니다."}, status=409)  # Conflict
        else:
            request.session['email_checked'] = True
            return JsonResponse({"success": True, "message": "사용 가능한 이메일입니다."})

    elif action == "check_password":
        if not password:
            request.session['password_checked'] = False
            return JsonResponse({"success": False, "message": "비밀번호를 입력해 주세요."}, status=400)
        elif password != password2:
            request.session['password_checked'] = False
            return JsonResponse({"success": False, "message": "비밀번호가 일치하지 않습니다."}, status=400)
        else:
            request.session['password_checked'] = True
            return JsonResponse({"success": True, "message": "비밀번호가 일치합니다."})

    elif action == "signup":
        if not all([email, password, password2, name, nickname]):
            return JsonResponse({"success": False, "message": "모든 항목을 입력해 주세요."}, status=400)

        if not is_valid_email(email):
            return JsonResponse({"success": False, "message": "올바른 이메일 형식이 아닙니다."}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "message": "이미 사용 중인 이메일입니다."}, status=409)

        if password != password2:
            return JsonResponse({"success": False, "message": "비밀번호가 일치하지 않습니다."}, status=400)

        if len(password) < 8:
            return JsonResponse({"success": False, "message": "비밀번호는 8자 이상이어야 합니다."}, status=400)

        if len(name) < 2:
            return JsonResponse({"success": False, "message": "이름은 2자 이상이어야 합니다."}, status=400)

        if len(nickname) < 1:
            return JsonResponse({"success": False, "message": "닉네임은 1자 이상이어야 합니다."}, status=400)

        user = User.objects.create_user(email=email, password=password, name=name, nickname=nickname)
        user.is_active = True
        request.session['email_checked'] = False
        request.session['password_checked'] = False

        return JsonResponse({"success": True, "message": "회원가입에 성공했습니다."})

    return JsonResponse({"success": False, "message": "잘못된 요청입니다."}, status=400)

def home_page_view(request):
    return render(request, 'homePage.html')

def login_page_view(request):
    return render(request, 'login.html')

def signup_page_view(request):
    return render(request, 'join.html')

def signup_complete_page_view(request):
    return render(request, 'joinComplete.html')