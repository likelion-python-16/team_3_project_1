from django.shortcuts import render
from rest_framework import permissions, viewsets

from .models import Review
from .serializers import ReviewSerializer

def review_list(request):
    return render(request, 'reviews/review_list.html')

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