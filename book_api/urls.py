from django.contrib import admin
from django.urls import path, include
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Book API",
        default_version='v1',
        description="A sample API for books, authors, and reviews",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@bookapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls), #admin페이지
    path('', views.index, name='index'),
    path("authors/", include("authors.urls")),  # 저자 페이지
    path("books/", include("books.urls")),      # 도서 페이지
    path("reviews/", include("reviews.urls")),  # 리뷰 페이지
    
    path("api/books/", include("books.api_urls")),      #도서 api
    path("api/reviews/", include("reviews.api_urls")),  #리뷰 api
    path("api/authors/", include("authors.api_urls")),  #저자 api

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]