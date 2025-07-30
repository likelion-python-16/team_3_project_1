from rest_framework import serializers
from .models import Book

from rest_framework import serializers
from .models import Book
from authors.models import Author

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author_id.author_name', read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), write_only=True)

    class Meta:
        model = Book
        fields = ('book_id', 'title', 'description', 'publication_date', 'created_at', 'author_id', 'author_name')
        