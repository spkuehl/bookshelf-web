from django.test import TestCase
from rentals.emails import send_confirmation
from django.core import mail

from books.models import Book
from rentals.models import Rental
from bookshelf.users.models import User
import datetime

class EmailTest(TestCase):
    """ Test module for Email Confirmations. """

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
            book = Book.objects.get(),
            due_date = datetime.date.today() + datetime.timedelta(5),
        )

    def test_send_confirmation_email(self):
        '''
        Ensure can send a rental confirmation email.
        '''
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
        'You have successfully rented A Storm of Swords, it is due on {}.'
        .format(datetime.date.today() + datetime.timedelta(5)))


class EmailIntegrationTest(TestCase):
    """ Test module for Email Confirmations via Book Model. """

    def setUp(self):
        self.book = Book.objects.create(
            title = 'A Storm of Swords',
            author = 'George RR Martin',
            publication_date=datetime.date.today() - datetime.timedelta(150)
        )
        self.user = User.objects.create_user(
            'utest',
            'utest@supass.com',
            'upass'
        )

    def test_send_confirmation_email_from_Book_model_method(self):
        '''
        Ensure Book.create_rental can create a Rental.
        '''
        # Create rental to trigger email.
        self.book.create_rental(self.user)

        # Get Rental to find due date
        rental = Rental.objects.get()

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Rental Confirmation: utest')

        # Verify that the body of the message is correct.
        self.assertEqual(mail.outbox[0].body,
        'You have successfully rented A Storm of Swords, it is due on {}.'
        .format(rental.due_date))
