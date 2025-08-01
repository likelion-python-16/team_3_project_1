from django.shortcuts import render
from django.db.models import Count
from django.http import JsonResponse
from authors.models import Author

def index(request):
    return render(request, 'index.html')