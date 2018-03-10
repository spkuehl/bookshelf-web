from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bookshelf.users.models import User
from books.models import Book


class CreateBookTest(APITestCase):
    """
    Tests /books create operations.
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


class DeleteUserBook(APITestCase):
    """
    Tests /books delete operations.
    """

    def setUp(self):
        self.book = Book.objects.create(
            title='The Golden Compass',
            author='Phillip Pullman')
        self.superuser = User.objects.create_superuser(
            'sutest',
            'sutest@supass.com',
            'supass'
        )
        self.client.login(username='sutest', password='supass')

    def test_can_delete_book(self):
        response = self.client.delete(reverse('book-detail', args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
