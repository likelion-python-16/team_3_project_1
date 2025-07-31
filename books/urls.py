from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='books/book_list.html'), name='book_list'),
    path('special/', views.special_books, name='special_books'),
]