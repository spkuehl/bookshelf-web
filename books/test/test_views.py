from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bookshelf.users.models import User
from books.models import Book
import datetime


class CreateBookTest(APITestCase):
    """
    Tests /books create operations.
    """

    def setUp(self):
        self.url = reverse('book-list')
        self.data = {'title': 'The Golden Compass',
                     'author': 'Phillip Pullman',
                     'publication_date': '2013-01-29',
        }
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


class DeleteBookTest(APITestCase):
    """
    Tests /books delete operations.
    """

    def setUp(self):
        self.book_one = Book.objects.create(
            title='The Golden Compass',
            author='Phillip Pullman',
            publication_date=datetime.date.today())

        self.book_two = Book.objects.create(
            title='The Subtle Knife',
            author='Phillip Pullman',
            publication_date=datetime.date.today())

        self.superuser = User.objects.create_superuser(
            'sutest',
            'sutest@supass.com',
            'supass'
        )

        self.client.login(username='sutest', password='supass')

    def test_can_delete_one_book(self):
        response = self.client.delete(reverse('book-detail', args=[self.book_one.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_can_delete_both_books(self):
        response = self.client.delete(reverse('book-detail', args=[self.book_one.id]))
        response = self.client.delete(reverse('book-detail', args=[self.book_two.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)


class UpdateBookTest(APITestCase):
    """
    Tests /books put operations.
    """

    def setUp(self):
        self.book = Book.objects.create(
            title='The Golden Compass',
            author='Phillip Pullman',
            publication_date=datetime.date.today())
        self.superuser = User.objects.create_superuser(
            'sutest',
            'sutest@supass.com',
            'supass'
        )
        self.data = {'author':'Phillip Pullman',
                     'title': 'The Northern Lights',
                     'publication_date':(datetime.date.today() - datetime.timedelta(120))}
        self.client.login(username='sutest', password='supass')

    def test_can_update_book(self):
        response = self.client.put(reverse('book-detail', args=[self.book.id]),  self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get().title, 'The Northern Lights')

    def test_can_transition_to_is_not_new(self):
        self.assertEqual(Book.objects.get().is_new(), True)
        response = self.client.put(reverse('book-detail', args=[self.book.id]),  self.data)
        self.assertEqual(Book.objects.get().is_new(), False)
