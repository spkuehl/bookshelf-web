from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book


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
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'The Golden Compass')
        self.assertEqual(Account.objects.get().author, 'Phillip Pullman')
