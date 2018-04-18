from django.test import TestCase
from rentals.emails import send_confirmation
from django.core import mail

from books.models import Book
from rentals.models import Rental
from bookshelf.users.models import User
import datetime

class EmailTest(TestCase):
    def setUp(self):
        Book.objects.create(
            title = 'A Storm of Swords',
            author = 'George RR Martin',
            publication_date=datetime.date.today() - datetime.timedelta(150)
        )
        User.objects.create_user(
            'utest',
            'utest@supass.com',
            'upass'
        )
        Rental.objects.create(
            id = 1,
            user = User.objects.get(),
            book = Book.objects.get(id=1),
            due_date = datetime.date.today() + datetime.timedelta(5),
        )

    def test_send_confirmation_email(self):
        user = User.objects.get()
        rental = Rental.objects.get(id=1)

        # Send message.
        send_confirmation(user=user, rental=rental)

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Rental Confirmation: utest')

        # Verify that the body of the message is correct.
        self.assertEqual(mail.outbox[0].body,
        'You have successfully rented A Storm of Swords, it is due on 2018-04-23.')
