from django.test import TestCase
from books.models import Book
from rentals.models import Rental
from bookshelf.users.models import User
import datetime

class RentalTest(TestCase):
    """ Test module for Rental Model. """

    def setUp(self):
        Book.objects.create(
            title = 'A Game of Thrones',
            author = 'George RR Martin',
            publication_date=datetime.date.today()
        )
        User.objects.create_user(
            'sutest',
            'sutest@supass.com',
            'supass'
        )
        Rental.objects.create(
            id = 1,
            user = User.objects.get(),
            book = Book.objects.get(),
            due_date = datetime.date.today() - datetime.timedelta(-5),
        )
        Rental.objects.create(
            id = 2,
            user = User.objects.get(),
            book = Book.objects.get(),
            due_date = datetime.date.today() - datetime.timedelta(5),
        )
        Rental.objects.create(
            id = 3,
            user = User.objects.get(),
            book = Book.objects.get(),
            due_date = datetime.date.today(),
        )
        Rental.objects.create(
            id = 4,
            user = User.objects.get(),
            book = Book.objects.get(),
            due_date = datetime.date.today(),
            date_returned = datetime.date.today(),
        )

    def test_string_representation(self):
        rental = Rental.objects.get(id=1)
        self.assertEqual(str(rental), 'A Game of Thrones %s' % datetime.date.today())

    def test_days_until_due_past_due_date(self):
        rental = Rental.objects.get(id=1)
        self.assertEqual(rental.days_until_due(), -5)

    def test_days_until_due_future_due_date(self):
        rental = Rental.objects.get(id=2)
        self.assertEqual(rental.days_until_due(), 5)

    def test_days_until_due_today_due_date(self):
        rental = Rental.objects.get(id=3)
        self.assertEqual(rental.days_until_due(), 0)

    def test_days_until_due_already_returned(self):
        rental = Rental.objects.get(id=4)
        self.assertEqual(rental.days_until_due(), None)
