from django.shortcuts import render
from django.db.models import Count
from django.http import JsonResponse
from authors.models import Author

def index(request):
    return render(request, 'index.html')

def author_book_count(request):
    author_stats = Author.objects.annotate(book_count=Count('book')).values('name', 'book_count')
    return JsonResponse(list(author_stats), safe=False)