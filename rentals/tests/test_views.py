from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bookshelf.users.models import User
from books.models import Book
from rentals.models import Rental
import datetime


class CreateRentalTest(APITestCase):
    """
    Tests /rentals create operations.
    """

    def setUp(self):
        self.url = reverse('rental-list')
        self.book = Book.objects.create(
            title='The Golden Compass',
            author='Phillip Pullman'
        )
        self.user = User.objects.create_superuser(
            'sutest',
            'sutest@supass.com',
            'supass'
        )
        self.data = {'book': self.book.id,
                     'user': self.user.id,
                     'due_date': datetime.date.today()
        }
        self.client.login(username='sutest', password='supass')

    def test_create_rental(self):
        """
        Ensure we can create a new Rental object.
        """

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rental.objects.count(), 1)


# class DeleteBookTest(APITestCase):
#     """
#     Tests /books delete operations.
#     """
#
#     def setUp(self):
#         self.book = Book.objects.create(
#             title='The Golden Compass',
#             author='Phillip Pullman')
#         self.superuser = User.objects.create_superuser(
#             'sutest',
#             'sutest@supass.com',
#             'supass'
#         )
#         self.client.login(username='sutest', password='supass')
#
#     def test_can_delete_book(self):
#         response = self.client.delete(reverse('book-detail', args=[self.book.id]))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Book.objects.count(), 0)
#
#
# class UpdateBookTest(APITestCase):
#     """
#     Tests /books put operations.
#     """
#
#     def setUp(self):
#         self.book = Book.objects.create(
#             title='The Golden Compass',
#             author='Phillip Pullman')
#         self.superuser = User.objects.create_superuser(
#             'sutest',
#             'sutest@supass.com',
#             'supass'
#         )
#         self.data = {'author':'Phillip Pullman', 'title': 'The Northern Lights'}
#         self.client.login(username='sutest', password='supass')
#
#     def test_can_update_book(self):
#         response = self.client.put(reverse('book-detail', args=[self.book.id]),  self.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Book.objects.get().title, 'The Northern Lights')
