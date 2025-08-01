from django.urls import path, include
from .views import book_list, book_detail, special_books
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'api', BookViewSet, basename='book')

urlpatterns = [
    path('', book_list, name='book_list'),
    path('<int:pk>/', book_detail, name='book_detail'),
    path('special/', special_books, name='special_books'),
    path('api/', include(router.urls)),
]