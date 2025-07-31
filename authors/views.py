from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Author
from .serializers import AuthorSerializer

from django.core.paginator import Paginator

def author_list(request):
    author_list = Author.objects.all()
    paginator = Paginator(author_list, 10)
    page_number = request.GET.get('page')
    authors = paginator.get_page(page_number)
    return render(request, 'authors/author_list.html', {'authors': authors})

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'authors/author_detail.html', {'author': author})

class AuthorListCreate(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'author_id'