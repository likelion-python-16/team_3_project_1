from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, review_list, review_detail

router = DefaultRouter()
router.register(r'api', ReviewViewSet, basename='review')

urlpatterns = [
    path('', review_list, name='review_list'),
    path('<int:pk>/', review_detail, name='review_detail'),
    path('api/', include(router.urls)),
]