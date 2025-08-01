from django.shortcuts import render, get_object_or_404
from rest_framework import permissions, viewsets

from .models import Review
from .serializers import ReviewSerializer

class IsReviewAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: #요청이 안전한 요청이면 그냥 권한을 부여합니다.
            return True

        if view.action in ['update', 'partial_update']: # 요청이 수정이면 작성자만 가능합니다.
            return obj.user == request.user

        if view.action == 'destroy':
            return obj.user == request.user or request.user.is_staff # 요청이 삭제라면 작성자와 관리자가 가능합니다.

        return False


def review_detail(request, pk): # 리뷰 상세 페이지 입니다.
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})

class ReviewViewSet(viewsets.ModelViewSet): # 클래스 기반 리뷰 뷰 입니다.
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Review.objects.all()
        book_id = self.request.query_params.get('book_id')
        if book_id is not None:
            queryset = queryset.filter(book_id=book_id)
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsReviewAuthorOrAdmin()]
        return [permissions.AllowAny()]