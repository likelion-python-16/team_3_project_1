from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path("authors/", include("authors.urls")),
    path("books/", include("books.urls")),
    path("reviews/", include("reviews.urls")),
    
    path("api/books/", include("books.api_urls")),
    path("api/reviews/", include("reviews.api_urls")),
    path("api/authors/", include("authors.api_urls")),
    path("api/dashboard/authors/", views.author_book_count, name='author_book_count'),
    
]
