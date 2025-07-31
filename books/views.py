from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from reviews.models import Review
from reviews.serializers import ReviewSerializer
from django.db.models import Avg, Count, StdDev, Case, When, Value, FloatField, F, Q
from django.db.models.functions import Sqrt

from django.core.paginator import Paginator

def book_list(request):
    book_list = Book.objects.all()
    paginator = Paginator(book_list, 10)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    return render(request, 'books/book_list.html', {'books': books})

def special_books(request):
    books = BookViewSet.queryset.all()[:10]
    return render(request, 'books/special_books.html', {'books': books})

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.annotate(
        review_count=Count('reviews', filter=Q(reviews__rating__isnull=False)),
        mean=Avg('reviews__rating', filter=Q(reviews__rating__isnull=False)),
        mean_sq=Avg(
            F('reviews__rating') * F('reviews__rating'),
            filter=Q(reviews__rating__isnull=False)
        ),
    ).annotate(
        rating_std_dev=Case(
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