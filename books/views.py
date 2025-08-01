from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from reviews.models import Review
from reviews.serializers import ReviewSerializer
from django.db.models import Avg, Count, Case, When, Value, FloatField, F, Q
from django.db.models.functions import Sqrt

from django.core.paginator import Paginator

def book_list(request): # 도서 관리 페이지 입니다.
    book_list = Book.objects.all()
    paginator = Paginator(book_list, 10)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, pk): # 도서 상세 페이지 입니다.
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})

def special_books(request): # 특별한 도서 페이지입니다.
    books = BookViewSet.queryset.all()[:10]
    return render(request, 'books/special_books.html', {'books': books})

class BookViewSet(viewsets.ModelViewSet): #클래스 기반 도서 뷰 입니다.

    def get_permissions(self):  # 권한을 부여합니다. 
        if self.request.method in permissions.SAFE_METHODS: # SAFE_METHODS에는 GET, HEAD, OPTIONS를 담고 있어 사용자의 요청이 이 중 하나라면 권한이 주어집니다.
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()] # SEFE_METHODS가 아니라면 관리자인지를 판별해 권한을 부여합니다.
    queryset = Book.objects.annotate( # 책 쿼리셋입니다.
        review_count=Count('reviews', filter=Q(reviews__rating__isnull=False)),
        mean=Avg('reviews__rating', filter=Q(reviews__rating__isnull=False)), 
        mean_sq=Avg(
            F('reviews__rating') * F('reviews__rating'),
            filter=Q(reviews__rating__isnull=False)
        ),
    ).annotate(
        rating_std_dev=Case( # 이는 특별한 책을 위해 해당 책의 리뷰 통계를 계산해 표준편차와 함께 응답합니다.
            When(
                review_count__gt=1,
                then=Sqrt(F('mean_sq') - F('mean') * F('mean'))
            ),
            default=Value(0.0),
            output_field=FloatField()
        )
    ).order_by('-rating_std_dev', 'title')
    serializer_class = BookSerializer

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        book = self.get_object()
        reviews = Review.objects.filter(book=book)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)