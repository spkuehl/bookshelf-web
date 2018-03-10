from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from books.models import Book


class BookAPITests(APITestCase):
    def test_create_book(self):
        """
        Ensure we can create a new Book object.
        """
        url = reverse('book-list')
        data = {'name': 'The Golden Compass',
                'author': 'Phillip Pullman'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().name, 'The Golden Compass')
        self.assertEqual(Book.objects.get().author, 'Phillip Pullman')
