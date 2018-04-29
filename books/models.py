from django.db import models
import datetime
import rentals
import rentals.emails as rental_emails
from django.shortcuts import get_object_or_404


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=40)
    is_rented = models.BooleanField(default=False)
    publication_date = models.DateField()

    def is_new(self):
        if self.publication_date > datetime.date.today() - datetime.timedelta(90):
            return True
        else:
            return False

    def rental_period(self):
        if self.is_new():
            return 7
        else:
            return 21

    def create_rental(self, user):
        # if request.user.is_authenticated():
            if self.is_rented:
                return None #Rental not created
            else:
                rental = rentals.models.Rental.objects.create(
                    user = user,
                    book = self,
                    due_date = datetime.date.today() + datetime.timedelta(self.rental_period()),
                )
                self.is_rented = True
                self.save()
                rental_emails.send_confirmation(user, rental)
                return rental #Rental created
        # else:
        #     return False #access denied

    def finish_rental(self, user):
        # if user.is_authenticated():
            if self.is_rented:
                rental = rentals.models.Rental.objects.get(
                    book=self, active_rental=True)
                rental.date_returned = datetime.date.today()
                rental.save()
                self.is_rented = False
                self.save()
                return rental #Rental is closed
            else:
                return None #Book is not rented
        # else:
        #     return None #access denied

    def renew_book(self, user, rental):
        # if user.is_authenticated():
        if rental.renewel_count < 3:
            if self.is_rented:
                rental.renewel_count += 1
                rental.due_date = datetime.date.today() + datetime.timedelta(self.rental_period())
                rental.save()
                return rental
            else:
                return None #Book is not rented
        else:
            return None #return error can not renew more than three times.
        # else:
        #     return None #access denied

    def create_reservation(self, user):
        # if request.user.is_authenticated():
            if self.is_rented:
                reservation = rentals.models.Reservation.objects.create(
                    user = user,
                    book = self,
                )
                # Reservation confirmation email
                return reservation #Rental created
            else:
                return None #Rental not created
        # else:
        #     return False #access denied

    def __str__(self):
        return self.title
