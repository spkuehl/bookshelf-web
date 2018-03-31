from django.test import TestCase
from bookshelf.users.models import User
from rentals.models import Rental
from books.models import Book
import datetime

class UserTest(TestCase):

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
        User.objects.create(
            username='spkuehl',
            password='pw'
        )

    def test_user_str_representation(self):
        user = User.objects.get(username='spkuehl')
        self.assertEqual(user.username, str(user))

    def test_user_has_no_overdue(self):
        book = Book.objects.get(id=1)
        user = User.objects.get(username='spkuehl')
        rental = book.create_rental(book=book, user=user)
        self.assertEqual(user.books_overdue(), 0)

    def test_user_has_no_rentals(self):
        user = User.objects.get(username='spkuehl')
        self.assertEqual(user.books_overdue(), 0)

    def test_user_has_one_overdue(self):
        book = Book.objects.get(id=1)
        user = User.objects.get(username='spkuehl')
        rental = book.create_rental(book=book, user=user)
        rental.due_date = datetime.date.today() + datetime.timedelta(-25)
        rental.save()
        self.assertEqual(user.books_overdue(), 1)

    def test_user_has_two_overdue(self):
        user = User.objects.get(username='spkuehl')
        book_one = Book.objects.get(id=1)
        book_two = Book.objects.get(id=2)
        rental_first = book_one.create_rental(book=book_one, user=user)
        rental_first.due_date = datetime.date.today() + datetime.timedelta(-25)
        rental_first.save()
        rental_second = book_two.create_rental(book=book_two, user=user)
        rental_second.due_date = datetime.date.today() + datetime.timedelta(-25)
        rental_second.save()
        self.assertEqual(user.books_overdue(), 2)
