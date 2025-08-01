from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from books.models import Book
from authors.models import Author
from .models import Review

User = get_user_model()

class ReviewPermissionsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpassword')
        self.author = Author.objects.create(author_name='Test Author')
        self.book = Book.objects.create(title='Test Book', description='Description', publication_date='2023-01-01', author_id=self.author)
        self.review1 = Review.objects.create(book=self.book, user=self.user1, rating=5, content='Great book!')
        self.review2 = Review.objects.create(book=self.book, user=self.user2, rating=4, content='Good book.')

    def test_unauthenticated_user_cannot_create_review(self):
        response = self.client.post('/api/reviews/', {'book': self.book.book_id, 'rating': 3, 'content': 'New review'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_create_review(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/api/reviews/', {'book': self.book.book_id, 'rating': 3, 'content': 'New review'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 3) # 2 existing + 1 new

    def test_authenticated_user_can_update_own_review(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(f'/api/reviews/{self.review1.review_id}/', {'content': 'Updated content'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review1.refresh_from_db()
        self.assertEqual(self.review1.content, 'Updated content')

    def test_authenticated_user_cannot_update_other_users_review(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(f'/api/reviews/{self.review2.review_id}/', {'content': 'Updated content'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_delete_own_review(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/reviews/{self.review1.review_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 1) # 2 existing - 1 deleted

    def test_authenticated_user_cannot_delete_other_users_review(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/reviews/{self.review2.review_id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_update_any_review(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(f'/api/reviews/{self.review1.review_id}/', {'content': 'Admin updated content'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_delete_any_review(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/reviews/{self.review1.review_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 1)

    def test_any_user_can_view_reviews(self):
        # Unauthenticated user
        response = self.client.get('/api/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        # Authenticated user
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)