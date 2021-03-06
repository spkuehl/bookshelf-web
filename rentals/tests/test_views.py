from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bookshelf.users.models import User
from books.models import Book
from rentals.models import Rental, Reservation
import datetime


class RentalAPITest(APITestCase):
    """
    Tests /rentals API Endpoint operations.
    """

    def setUp(self):
        self.url = reverse('rental-list')
        self.book = Book.objects.create(
            title='The Golden Compass',
            author='Phillip Pullman',
            publication_date=datetime.date.today()
        )
        self.user = User.objects.create_user(
            'utest',
            'utest@upass.com',
            'upass'
        )
        self.data = {'book': self.book.id,
                     'user': self.user.id,
                     'due_date': datetime.date.today()
        }
        self.rental = Rental.objects.create(
            user = self.user,
            book = self.book,
            due_date = datetime.date.today()
        )
        self.new_date = datetime.date.today() + datetime.timedelta(1)
        self.data = {'user': self.user.id,
                     'book': self.book.id,
                     'due_date': self.new_date
        }

    def test_user_can_create_rental(self):
        """
        Ensure user can create a new Rental object.
        """
        self.client.login(username='utest', password='upass')
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rental.objects.count(), 2)

    def test_user_can_delete_rental(self):
        """
        Ensure user can delete a Rental object.
        """
        self.client.login(username='utest', password='upass')
        response = self.client.delete(reverse('rental-detail', args=[self.rental.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Rental.objects.count(), 0)

    def test_user_can_update_rental(self):
        """
        Ensure user can update a new Rental object.
        """
        self.client.login(username='utest', password='upass')
        response = self.client.put(reverse('rental-detail', args=[self.rental.id]),  self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Rental.objects.get().due_date, self.new_date)


class ReservationAPITest(APITestCase):
    """
    Tests /reservations API endpoint operations.
    """
    def setUp(self):
        self.url = reverse('reservation-list')
        self.book = Book.objects.create(
            title='The Golden Compass',
            author='Phillip Pullman',
            publication_date=datetime.date.today(),
            is_rented=True
        )
        self.unreserved_book = Book.objects.create(
            title='The Amber Spyglass',
            author='Phillip Pullman',
            publication_date=datetime.date.today(),
            is_rented=True
        )
        self.user = User.objects.create_user(
            'utest',
            'utest@upass.com',
            'upass'
        )
        self.data = {'book': self.unreserved_book.id,
                     'user': self.user.id,
        }
        self.reservation = Reservation.objects.create(
            user = self.user,
            book = self.book,
        )

    def test_user_can_create_reservation(self):
        """
        Ensure user can create a new Reservation object.
        """
        self.client.login(username='utest', password='upass')
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 2)

    def test_user_can_delete_reservation(self):
        """
        Ensure user can delete a Reservation object.
        """
        self.client.login(username='utest', password='upass')
        response = self.client.delete(reverse('reservation-detail', args=[self.reservation.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reservation.objects.count(), 0)

    # Test can update reservation?



class ReservationQueueTest(APITestCase):
    """
    Tests the correct queue length is retrieved.
    """
    def setUp(self):
        self.book = Book.objects.create(
            title='The Golden Compass',
            author='Phillip Pullman',
            publication_date=datetime.date.today(),
            is_rented=True
        )
        self.user = User.objects.create_user(
            'utest',
            'utest@upass.com',
            'upass'
        )
        self.first_user_in_line = User.objects.create_user(
            'first_user_in_line',
            'utest@upass.com',
            'upass'
        )
        self.third_user_in_line = User.objects.create_user(
            'third_user_in_line',
            'utest@upass.com',
            'upass'
        )
        self.reservation_1 = Reservation.objects.create(
            user = self.first_user_in_line,
            book = self.book,
        )
        self.reservation_2 = Reservation.objects.create(
            user = self.user,
            book = self.book,
        )
        self.reservation_3 = Reservation.objects.create(
            user = self.third_user_in_line,
            book = self.book,
        )

    def test_reservation_list(self):
        """
        Ensure the correct queue length is retrieved.
        """
        self.assertEqual(Reservation.objects.count(), 3)
        self.assertEqual(self.reservation_1.place_in_line(), 0)
        self.assertEqual(self.reservation_2.place_in_line(), 1)
        self.assertEqual(self.reservation_3.place_in_line(), 2)
