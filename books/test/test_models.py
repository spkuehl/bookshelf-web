from django.test import TestCase
from books.models import Book
import datetime
from bookshelf.users.models import User
from rentals.models import Rental

class BookTest(TestCase):
    """ Test module for Book Model. """

    def setUp(self):
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

    def test_string_representation(self):
        book = Book.objects.get(id=1)
        self.assertEqual(str(book), book.title)

    def test_book_is_new(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.is_new(), True)

    def test_book_is_not_new(self):
        book = Book.objects.get(id=2)
        self.assertEqual(book.is_new(), False)

    def test_rental_period_is_7(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.rental_period(), 7)

    def test_rental_period_is_21(self):
        book = Book.objects.get(id=2)
        self.assertEqual(book.rental_period(), 21)

    def test_create_rental_from_book_method(self):
        book = Book.objects.get(id=1)
        user = User.objects.get()
        self.assertEqual(Rental.objects.count(), 0)
        book.create_rental(book=book, user=user)
        self.assertEqual(Rental.objects.count(), 1)
        self.assertEqual(book.is_rented, True)

    def test_can_not_rent_book_already_rented(self):
        book = Book.objects.get(id=1)
        user = User.objects.get()
        book.create_rental(book=book, user=user)
        rental = book.create_rental(book=book, user=user)
        self.assertEqual(rental, None)

    def test_finish_rental_from_book_method(self):
        book = Book.objects.get(id=1)
        user = User.objects.get()
        rental = book.create_rental(book=book, user=user)
        book.finish_rental(book=book, user=user, rental=rental)
        self.assertEqual(rental.date_returned, datetime.date.today())
        self.assertEqual(book.is_rented, False)

    def test_renew_book(self):
        book = Book.objects.get(id=1)
        user = User.objects.get()
        rental = book.create_rental(book=book, user=user)
        book.renew_book(book=book, user=user, rental=rental)
        self.assertEqual(rental.renewel_count, 1)

    def test_can_not_renew_book_over_3_times(self):
        book = Book.objects.get(id=1)
        user = User.objects.get()
        rental = book.create_rental(book=book, user=user)
        book.renew_book(book=book, user=user, rental=rental)
        book.renew_book(book=book, user=user, rental=rental)
        book.renew_book(book=book, user=user, rental=rental)
        fourth_try = book.renew_book(book=book, user=user, rental=rental)
        self.assertEqual(rental.renewel_count, 3)
        self.assertEqual(fourth_try, None)
