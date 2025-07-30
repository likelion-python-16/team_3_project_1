from django.urls import path
from . import views

urlpatterns = [
    path('', views.author_list, name='author_list'),
    path('<int:author_id>/', views.author_detail, name='author_detail'), 
    path('api/', views.AuthorListCreate.as_view(), name='author-list-create'),
    path('api/<int:id>/', views.AuthorRetrieveUpdateDestroy.as_view(), name='author-retrieve-update-destroy'),
]