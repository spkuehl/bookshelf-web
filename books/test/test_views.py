from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bookshelf.users.models import User
from books.models import Book


class CreateBookTest(APITestCase):
    """
    Tests /books list operations.
    """

    def setUp(self):
        self.url = reverse('book-list')
        self.data = {'title': 'The Golden Compass',
                     'author': 'Phillip Pullman'}
        self.superuser = User.objects.create_superuser(
            'sutest',
            'sutest@supass.com',
            'supass'
        )
        self.client.login(username='sutest', password='supass')

    def test_create_book(self):
        """
        Ensure we can create a new Book object.
        """

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'The Golden Compass')
        self.assertEqual(Book.objects.get().author, 'Phillip Pullman')
