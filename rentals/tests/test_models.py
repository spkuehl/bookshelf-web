from django.test import TestCase
from books.models import Book
from rentals.models import Rental, Reservation
from bookshelf.users.models import User
import datetime

class RentalTest(TestCase):
    """ Test module for Rental Model. """

    def setUp(self):
        Book.objects.create(
            id = 1,
            title = 'A Game of Thrones',
            author = 'George RR Martin',
            publication_date=datetime.date.today()
        )
        Book.objects.create(
            id = 2,
            title = 'A Storm of Swords',
            author = 'George RR Martin',
            publication_date=datetime.date.today() - datetime.timedelta(150)
        )
        User.objects.create_user(
            'sutest',
            'sutest@supass.com',
            'supass'
        )
        Rental.objects.create(
            id = 1,
            user = User.objects.get(),
            book = Book.objects.get(id=1),
            due_date = datetime.date.today() - datetime.timedelta(-5),
        )
        Rental.objects.create(
            id = 2,
            user = User.objects.get(),
            book = Book.objects.get(id=1),
            due_date = datetime.date.today() - datetime.timedelta(5),
        )
        Rental.objects.create(
            id = 3,
            user = User.objects.get(),
            book = Book.objects.get(id=1),
            due_date = datetime.date.today(),
        )
        Rental.objects.create(
            id = 4,
            user = User.objects.get(),
            book = Book.objects.get(id=2),
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

    def test_rental_period_is_7(self):
        rental = Rental.objects.get(id=1)
        self.assertEqual(rental.book.rental_period(), 7)

    def test_rental_period_is_21(self):
        rental = Rental.objects.get(id=4)
        self.assertEqual(rental.book.rental_period(), 21)


class ReservationTest(TestCase):
    """ Test module for Reservation Model. """

    def setUp(self):
        self.rented_book = Book.objects.create(
            id = 1,
            title = 'A Game of Thrones',
            author = 'George RR Martin',
            publication_date=datetime.date.today()
        )
        self.unrented_book = Book.objects.create(
            id = 2,
            title = 'A Feast For Crows',
            author = 'George RR Martin',
            publication_date=datetime.date.today()
        )
        self.user = User.objects.create_user('utest','upass')
        self.rental = Rental.objects.create(
            id = 1,
            user = User.objects.get(),
            book = Book.objects.get(id=1),
            due_date = datetime.date.today() + datetime.timedelta(5),
        )

    def test_can_not_create_reservation_on_unrented_book(self):
        Reservation.objects.create(user = self.user, book = self.unrented_book)
        self.assertEqual(list(Reservation.objects.all()), [])
