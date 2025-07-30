# reviews/serializers.py
from rest_framework import serializers
from .models import Review
from books.models import Book # Import Book model

class ReviewSerializer(serializers.ModelSerializer):
    review_id = serializers.IntegerField(read_only=True)
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    book_title = serializers.CharField(source='book.title', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    content = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Review
        fields = ('review_id', 'book', 'book_title', 'user_id', 'username', 'rating', 'content', 'created_at')

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.book = validated_data.get('book', instance.book)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
