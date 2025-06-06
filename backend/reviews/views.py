from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from countries.models import Embassy
from .models import Review, Helpfulness
from django.utils import timezone

@require_POST
@login_required
def created_review(request, embassy_id): # 후기 작성
    embassy = get_object_or_404(Embassy, id=embassy_id)
    content = request.POST.get("content", "").strip() # 빈 문자열 제거
    if content:
        Review.objects.create(user=request.user, embassy=embassy, content=content, created_at=timezone.now()) # auto_now_add지만 명시해줌
    return redirect("countries:country_detail", slug=embassy.slug) # 후기 작성 후 상세 페이지로 리다이렉트

@require_POST
@login_required
def delete_review(request, review_id): # 후기 삭제
    review = get_object_or_404(Review, id=review_id)
    if request.user == review.user:
        review.delete()
        return redirect("countries:country_detail", slug=review.embassy.slug)
    return HttpResponseForbidden # 본인 글이 아닐 경우 삭제 금지

@require_POST
@login_required
def toggle_helpful(request, review_id): # 도움돼요 토글 기능 (좋아요/취소)
    review = get_object_or_404(Review, id=review_id)
    if request.user == review.user:
        return HttpResponseForbidden  # 본인 글에는 도움 누를 수 없음

    existing = Helpfulness.objects.filter(user=request.user, review=review)
    if existing.exists():
        existing.delete() # 이미 누른 경우 취소
    else:
        Helpfulness.objects.create(user=request.user, review=review) # 없으면 새로 생성
    return redirect("countries:country_detail", slug=review.embassy.slug)

@require_POST
@login_required
def update_review(request, review_id): # 후기 수정
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return HttpResponseForbidden() # 본인 글이 아닌 경우 수정 금지

    content = request.POST.get("content", "").strip()
    if content:
        review.content = content
        review.save()
    return redirect("countries:country_detail", slug=review.embassy.slug)
