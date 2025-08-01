from django.urls import path, include
from .views import book_list, book_detail, special_books
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'api', BookViewSet, basename='book')

urlpatterns = [
    path('', book_list, name='book_list'),                  # 도서 관리 페이지
    path('<int:pk>/', book_detail, name='book_detail'),     # 도서 상세 페이지
    path('special/', special_books, name='special_books'),  # 특별한 도서 페이지
    path('api/', include(router.urls)),                     # 도서 api
]