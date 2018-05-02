from django.test import TestCase
from books.models import Book
import datetime
from bookshelf.users.models import User
from rentals.models import Rental, Reservation
from django.urls import reverse
from rest_framework import status


class BookAPITest(TestCase):
    """ Test module for Book API Endpoints. """

    def setUp(self):
        self.book = Book.objects.create(
            id=1,
            title='Game of Thrones',
            author='George RR Martin',
            publication_date=datetime.date.today()
        )
        User.objects.create_superuser(
            'utest',
            'super@test',
            'upass'
        )
        self.client.login(username='utest', password='upass')

    def test_checkout_book_endpoint(self):
        """
        Ensure we can create a rental from the book-checkout endpoint.
        """
        url = reverse('book-checkout', kwargs={'pk': self.book.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_not_checkout_book_already_rented_endpoint(self):
        """
        Ensure we can not create a rental (already out) from the book-checkout
        endpoint.
        """
        self.book.is_rented = True
        url = reverse('book-checkout', kwargs={'pk': self.book.id})
        response = self.client.post(url)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_checkin_book_endpoint(self):
        """
        Ensure we can finish a rental from the book-checkin endpoint.
        """
        checkout_url = reverse('book-checkout', kwargs={'pk': self.book.id})
        response_url = self.client.post(checkout_url)
        url = reverse('book-checkin', kwargs={'pk': self.book.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_can_not_checkin_unrented_book_endpoint(self):
        """
        Ensure we can not finish create a rental (already out) from the
        book-checkin endpoint.
        """
        url = reverse('book-checkin', kwargs={'pk': self.book.id})
        response = self.client.post(url)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReservationAPITest(TestCase):
    """ Test module for Reservation Book API Endpoints. """

    def setUp(self):
        self.book = Book.objects.create(
            id=1,
            title='Game of Thrones',
            author='George RR Martin',
            publication_date=datetime.date.today(),
            is_rented=True
        )
        User.objects.create_superuser(
            'utest',
            'super@test',
            'upass'
        )
        self.client.login(username='utest', password='upass')

    def test_reserve_book_endpoint(self):
        """
        Ensure we can create a reservation from the api endpoint.
        """
        url = reverse('book-reservation', kwargs={'pk': self.book.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_not_reserve_book_it_isnt_rented_endpoint(self):
        """
        Ensure we can not create a reservation from the book-reservation
        endpoint if it is available to rent.
        """
        self.book.is_rented = False
        self.book.save()
        url = reverse('book-reservation', kwargs={'pk': self.book.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RenewAPITest(TestCase):
    """ Test module for Renew Book API Endpoints. """

    def setUp(self):
        self.book = Book.objects.create(
            id=1,
            title='Game of Thrones',
            author='George RR Martin',
            publication_date=datetime.date.today(),
            is_rented=False
        )
        User.objects.create_superuser(
            'utest',
            'super@test',
            'upass'
        )
        self.client.login(username='utest', password='upass')

    def test_renew_book_endpoint(self):
        """
        Ensure we can create a renewal from the api endpoint.
        """
        checkout_url = reverse('book-checkout', kwargs={'pk': self.book.id})
        checkout_response = self.client.post(checkout_url)
        rental = Rental.objects.get(book=self.book, active_rental=True)
        rental.due_date = datetime.date.today()
        self.assertEqual(rental.due_date, datetime.date.today())
        url = reverse('book-renew', kwargs={'pk': self.book.id})
        response = self.client.post(url)
        rental = Rental.objects.get(book=self.book, active_rental=True)
        self.assertEqual(rental.due_date, datetime.date.today()+datetime.timedelta(self.book.rental_period()))
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(rental.renewel_count, 1)

    def test_can_not_renew_book_over_3_times_endpoint(self):
        """
        Ensure we can create a renewal from the api endpoint.
        """
        checkout_url = reverse('book-checkout', kwargs={'pk': self.book.id})
        checkout_response = self.client.post(checkout_url)
        rental = Rental.objects.get(book=self.book, active_rental=True)
        url = reverse('book-renew', kwargs={'pk': self.book.id})
        response = self.client.post(url)
        response = self.client.post(url)
        response = self.client.post(url)
        response = self.client.post(url)
        rental = Rental.objects.get(book=self.book, active_rental=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(rental.renewel_count, 3)
