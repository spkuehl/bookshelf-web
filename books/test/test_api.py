from django.test import TestCase
from books.models import Book
import datetime
from bookshelf.users.models import User
from rentals.models import Rental
from django.urls import reverse


class BookAPITest(TestCase):
    """ Test module for Book Model. """

    def setUp(self):
        self.url = reverse('book-checkout')
        Book.objects.create(
            id=1,
            title='Game of Thrones',
            author='George RR Martin',
            publication_date=datetime.date.today()
        )
        Book.objects.create(
            id=2,
            title='Game of Thrones',
            author='George RR Martin',
            publication_date=datetime.date.today() - datetime.timedelta(100)
        )
        User.objects.create_user(
            'utest',
            'upass'
        )
        self.client.login(username='sutest', password='supass')

    def test_checkout_book_endpoint(self):
        """
        Ensure we can create a rental from the book-checkout endpoint.
        """
        response = self.client.post(self.url, self.book, format='json')
