from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='authors/author_list.html'), name='author_list'),
    path('<int:author_id>/', views.author_detail, name='author_detail'), 
    path('api/', views.AuthorListCreate.as_view(), name='author-list-create'),
    path('api/<int:id>/', views.AuthorRetrieveUpdateDestroy.as_view(), name='author-retrieve-update-destroy'),
]