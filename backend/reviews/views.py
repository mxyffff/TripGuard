from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json

from countries.models import Embassy
from .models import Review, Helpfulness

@csrf_exempt
@require_POST
@login_required
def create_review_api(request, slug):
    """
    [POST] 특정 공관에 대한 후기를 작성하는 API

    - 요청 URL 예시: /reviews/create/3/
    - 요청 방식: POST
    - 요청 데이터 예시: { content: "좋았어요!" }

    - 필수 조건:
        - 로그인한 사용자만 가능
        - 후기 내용(content)이 공백이 아니어야 함
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "잘못된 요청 형식입니다."}, status=400)

    content = data.get("content", "").strip()
    if not content:
        return JsonResponse({"error": "내용이 비어 있습니다."}, status=400)

    embassies = Embassy.objects.filter(slug=slug)
    if not embassies.exists():
        return JsonResponse({"error": "해당 slug의 공관이 존재하지 않습니다."}, status=404)

    # '대사관'이 포함된 공관 우선 선택
    embassy = (
            embassies.filter(embassy_name__icontains="대사관").first()
            or embassies.first()
    )

    review = Review.objects.create(
        user=request.user,
        embassy=embassy,
        content=content,
    )

    return JsonResponse({
        "message": "후기 등록 성공",
        "review": {
            "id": review.id,
            "nickname": review.user.nickname,
            "content": review.content,
            "created_at": review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": review.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            "helpfulness": 0,
        }
    })


@csrf_exempt
@require_POST
@login_required
def delete_review_api(request, review_id):
    """
    [POST] 로그인한 사용자가 본인의 후기를 삭제하는 API

    - 요청 URL 예시: /reviews/delete/5/
    - 요청 방식: POST
    - 필수 조건: 본인 후기만 삭제 가능
    """
    review = get_object_or_404(Review, id=review_id)

    if request.user != review.user:
        return HttpResponseForbidden("본인 후기만 삭제할 수 있습니다.")

    review.delete()

    return JsonResponse({"message": "후기 삭제 완료"})

@csrf_exempt
@require_POST
@login_required
def update_review_api(request, review_id):
    """
    [POST] 로그인한 사용자가 본인의 후기를 수정하는 API

    - 요청 URL 예시: /reviews/update/5/
    - 요청 데이터 예시: { content: "수정된 후기입니다" }
    - 필수 조건:
        - 본인 후기만 수정 가능
        - 수정 내용이 공백이 아니어야 함
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "잘못된 요청 형식입니다."}, status=400)

    content = data.get("content", "").strip()
    if not content:
        return JsonResponse({"error": "수정할 내용이 비어 있습니다."}, status=400)

    review = get_object_or_404(Review, id=review_id)

    if request.user != review.user:
        return HttpResponseForbidden("본인 후기만 수정할 수 있습니다.")

    review.content = content
    review.updated_at = timezone.now()
    review.save()

    return JsonResponse({
        "message": "후기 수정 완료",
        "updated_review": {
            "id": review.id,
            "nickname": request.user.nickname,
            "content": review.content,
            "updated_at": review.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    })

@csrf_exempt
@require_POST
@login_required
def toggle_helpful_api(request, review_id):
    """
    [POST] '도움돼요' 상태를 토글하는 API

    - 요청 URL 예시: /reviews/helpful/5/
    - 필수 조건:
        - 본인 후기에는 도움 누를 수 없음
        - 한 번 누르면 등록되고, 다시 누르면 취소됨
    """
    # 실제로 body 안 쓰더라도, 오류 방지를 위해 dummy로 한 번 파싱
    try:
        if request.headers.get("Content-Type") == "application/json":
            json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "요청 데이터 형식이 잘못되었습니다."}, status=400)

    review = get_object_or_404(Review, id=review_id)

    if request.user == review.user:
        return JsonResponse({"error": "자신의 댓글엔 좋아요를 누를 수 없습니다."}, status=403)

    existing = Helpfulness.objects.filter(user=request.user, review=review)

    if existing.exists():
        existing.delete()
        is_helpful = False
    else:
        Helpfulness.objects.create(user=request.user, review=review)
        is_helpful = True

    return JsonResponse({
        "message": "도움 상태 변경 완료",
        "is_helpful": is_helpful,
        "helpfulness_count": review.helpfulness.all().count()
    })

