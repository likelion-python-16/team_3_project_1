from django.urls import path
from authors import views

urlpatterns = [
    path('', views.AuthorListCreate.as_view(), name='author-list-create'),
    path('<int:author_id>/', views.AuthorRetrieveUpdateDestroy.as_view(), name='author-retrieve-update-destroy'),
]