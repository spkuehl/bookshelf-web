from django.test import TestCase
from books.models import Book
import datetime

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

    def test_string_representation(self):
        book = Book.objects.get(id=1)
        self.assertEqual(str(book), book.title)

    def test_book_is_new(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.is_new(), True)

    def test_book_is_not_new(self):
        book = Book.objects.get(id=2)
        self.assertEqual(book.is_new(), False)
