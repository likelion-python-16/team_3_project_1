from django.shortcuts import render, get_object_or_404
from rest_framework import permissions, viewsets

from .models import Review
from .serializers import ReviewSerializer

from django.core.paginator import Paginator

def review_list(request):
    review_list = Review.objects.all()
    paginator = Paginator(review_list, 10)
    page_number = request.GET.get('page')
    reviews = paginator.get_page(page_number)
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})

class ReviewViewSet(viewsets.ModelViewSet):
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
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]