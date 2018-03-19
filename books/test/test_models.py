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

    def test_string_representation(self):
        book = Book.objects.get(id=1)
        self.assertEqual(str(book), book.title)
