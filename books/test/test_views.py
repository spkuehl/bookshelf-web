from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bookshelf.users.models import User
from books.models import Book
import datetime


class BookAPITests(APITestCase):
    def setUp(self):
        self.url = reverse('book-list')
        self.book_one = Book.objects.create(
            title='The Golden Compass',
            author='Phillip Pullman',
            publication_date=datetime.date.today())

        self.book_two = Book.objects.create(
            title='The Subtle Knife',
            author='Phillip Pullman',
            publication_date=datetime.date.today())
        self.data = {'title': 'The Amber Spyglass',
                     'author': 'Phillip Pullman',
                     'publication_date': '2013-01-29',
        }
        self.new_data = {'title': 'The Northern Lights',
                         'author':'Phillip Pullman',
                         'publication_date':'2013-01-29',
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
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(id=3).title, 'The Amber Spyglass')
        self.assertEqual(Book.objects.get(id=3).author, 'Phillip Pullman')

    def test_can_delete_one_book(self):
        """
        Ensure we can delete a one Book object.
        """
        response = self.client.delete(reverse('book-detail', args=[self.book_one.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_can_delete_both_books(self):
        """
        Ensure we can delete all Book objects.
        """
        response = self.client.delete(reverse('book-detail', args=[self.book_one.id]))
        response = self.client.delete(reverse('book-detail', args=[self.book_two.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_can_update_book(self):
        """
        Ensure we can update a Book object.
        """
        response = self.client.put(reverse('book-detail', args=[self.book_one.id]), self.new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(id=self.book_one.id).title, 'The Northern Lights')

    # Test conditions in which model methods will be changed through Updates
