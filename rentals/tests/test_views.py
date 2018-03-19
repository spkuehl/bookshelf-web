from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bookshelf.users.models import User
from books.models import Book
from rentals.models import Rental
import datetime


class CreateRentalTest(APITestCase):
    """
    Tests /rentals create operations.
    """

    def setUp(self):
        self.url = reverse('rental-list')
        self.book = Book.objects.create(
            title='The Golden Compass',
            author='Phillip Pullman',
            publication_date=datetime.date.today()
        )
        self.user = User.objects.create_superuser(
            'sutest',
            'sutest@supass.com',
            'supass'
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

    def test_create_rental(self):
        """
        Ensure we can create a new Rental object.
        """
        self.client.login(username='sutest', password='supass')
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rental.objects.count(), 1)

    def test_user_can_not_create_rental(self):
        self.client.login(username='utest', password='upass')
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DeleteRentalTest(APITestCase):
    """
    Tests /rentals delete operations.
    """

    def setUp(self):
        self.url = reverse('rental-list')
        self.book = Book.objects.create(
            title='The Golden Compass',
            author='Phillip Pullman',
            publication_date=datetime.date.today()
        )
        self.user = User.objects.create_superuser(
            'sutest',
            'sutest@supass.com',
            'supass'
        )
        self.user = User.objects.create_user(
            'utest',
            'utest@upass.com',
            'upass'
        )
        self.rental = Rental.objects.create(
            user = self.user,
            book = self.book,
            due_date = datetime.date.today()
        )

    def test_can_delete_rental(self):
        self.client.login(username='sutest', password='supass')
        response = self.client.delete(reverse('rental-detail', args=[self.rental.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Rental.objects.count(), 0)

    def test_user_can_not_delete_rental(self):
        self.client.login(username='utest', password='upass')
        response = self.client.delete(reverse('rental-detail', args=[self.rental.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UpdateRentalTest(APITestCase):
    """
    Tests /rentals put operations.
    """

    def setUp(self):
        self.url = reverse('rental-list')
        self.book = Book.objects.create(
            title='The Golden Compass',
            author='Phillip Pullman',
            publication_date=datetime.date.today()

        )
        self.user = User.objects.create_superuser(
            'sutest',
            'sutest@supass.com',
            'supass'
        )
        self.user = User.objects.create_user(
            'utest',
            'utest@upass.com',
            'upass'
        )
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

    def test_admin_can_update_rental(self):
        self.client.login(username='sutest', password='supass')
        response = self.client.put(reverse('rental-detail', args=[self.rental.id]),  self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Rental.objects.get().due_date, self.new_date)

    def test_user_can_not_update_rental(self):
        self.client.login(username='utest', password='upass')
        response = self.client.put(reverse('rental-detail', args=[self.rental.id]),  self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
