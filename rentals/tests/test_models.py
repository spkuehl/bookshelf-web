from django.test import TestCase
from books.models import Book
from rentals.models import Rental
from bookshelf.users.models import User
import datetime

class RentalTest(TestCase):
    """ Test module for Rental Model. """

    def setUp(self):
        Book.objects.create(
            id = 1,
            title = 'Game of Thrones',
            author = 'George RR Martin'
        )
        User.objects.create_user(
            'sutest',
            'sutest@supass.com',
            'supass'
        )
        Rental.objects.create(
            user = User.objects.get(),
            book = Book.objects.get(id=1),
            due_date = datetime.date.today()
        )

    def test_string_representation(self):
        rental = Rental.objects.get(id=1)
        self.assertEqual(str(rental), 'Game of Thrones %s' % datetime.date.today())

    # More testing needed. Due Date & Renewel Count, etc.
