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
