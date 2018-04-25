from django.test import TestCase
from books.models import Book
import datetime
from bookshelf.users.models import User
from rentals.models import Rental
from django.urls import reverse
from rest_framework import status


class BookAPITest(TestCase):
    """ Test module for Book API Endpoints. """

    def setUp(self):
        self.book = Book.objects.create(
            id=1,
            title='Game of Thrones',
            author='George RR Martin',
            publication_date=datetime.date.today()
        )
        User.objects.create_superuser(
            'utest',
            'super@test',
            'upass'
        )
        self.client.login(username='utest', password='upass')

    def test_checkout_book_endpoint(self):
        """
        Ensure we can create a rental from the book-checkout endpoint.
        """
        url = reverse('book-checkout', kwargs={'pk': self.book.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_not_checkout_book_already_rented_endpoint(self):
        """
        Ensure we can not create a rental (already out) from the book-checkout endpoint.
        """
        self.book.is_rented = True
        url = reverse('book-checkout', kwargs={'pk': self.book.id})
        response = self.client.post(url)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
