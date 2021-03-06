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
            due_date = datetime.date.today() + datetime.timedelta(-5),
        )
        Rental.objects.create(
            id = 2,
            user = User.objects.get(),
            book = Book.objects.get(id=1),
            due_date = datetime.date.today() + datetime.timedelta(5),
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
        '''
        Ensure we display the correct string representation for Rental Objects.
        '''
        rental = Rental.objects.get(id=1)
        self.assertEqual(str(rental), 'A Game of Thrones %s' % datetime.date.today())

    def test_days_until_due_past_due_date(self):
        '''
        Ensure we properly compute a negative days until due value for Rental Objects.
        '''
        rental = Rental.objects.get(id=1)
        self.assertEqual(rental.days_until_due(), -5)

    def test_days_until_due_future_due_date(self):
        '''
        Ensure we properly compute a positive days until due value for Rental Objects.
        '''
        rental = Rental.objects.get(id=2)
        self.assertEqual(rental.days_until_due(), 5)

    def test_days_until_due_today_due_date(self):
        '''
        Ensure we properly compute a zero days until due value for Rental Objects.
        '''
        rental = Rental.objects.get(id=3)
        self.assertEqual(rental.days_until_due(), 0)

    def test_days_until_due_already_returned(self):
        '''
        Ensure we properly return None for Rental Objects already returned.
        '''
        rental = Rental.objects.get(id=4)
        self.assertEqual(rental.days_until_due(), None)

    def test_rental_period_is_7(self):
        '''
        Ensure rental period is 7 for new books.
        '''
        rental = Rental.objects.get(id=1)
        self.assertEqual(rental.book.rental_period(), 7)

    def test_rental_period_is_21(self):
        '''
        Ensure rental period is 21 for old books.
        '''
        rental = Rental.objects.get(id=4)
        self.assertEqual(rental.book.rental_period(), 21)


class ReservationTest(TestCase):
    """ Test module for Reservation Model. """

    def setUp(self):
        self.rented_book = Book.objects.create(
            id = 1,
            title = 'A Game of Thrones',
            author = 'George RR Martin',
            publication_date=datetime.date.today(),
            is_rented = True
        )
        self.unrented_book = Book.objects.create(
            id = 2,
            title = 'A Feast For Crows',
            author = 'George RR Martin',
            publication_date=datetime.date.today()
        )
        self.user = User.objects.create_user('utest','upass')
        self.unrenting_user = User.objects.create_user('u2test','u2pass')
        self.rental = Rental.objects.create(
            id = 1,
            user = User.objects.get(username='utest'),
            book = Book.objects.get(id=1),
            due_date = datetime.date.today() + datetime.timedelta(5),
        )

    def test_can_create_reservation_on_rented_book(self):
        '''
        Ensure we can create a Reservation Object.
        '''
        Reservation.objects.create(user = self.unrenting_user, book = self.rented_book)
        self.assertEqual(len(Reservation.objects.all()), 1)

    def test_can_not_create_reservation_on_unrented_book(self):
        '''
        Ensure we can not create a Reservation Object on an unrented (available) Book.
        '''
        Reservation.objects.create(user = self.user, book = self.unrented_book)
        self.assertEqual(list(Reservation.objects.all()), [])

    def test_can_not_be_in_queue_more_than_once(self):
        '''
        Ensure a User can not be in Reservation queue more than once per Book.
        '''
        Reservation.objects.create(user = self.unrenting_user, book = self.rented_book)
        Reservation.objects.create(user = self.unrenting_user, book = self.rented_book)
        self.assertEqual(len(Reservation.objects.all()), 1)
