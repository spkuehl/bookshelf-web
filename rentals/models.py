from django.db import models
from books.models import Book
from bookshelf.users.models import User
from django.core.validators import MaxValueValidator
import datetime

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=False, blank=False)
    date_returned = models.DateField(null=True, blank=True)
    renewel_count = models.PositiveIntegerField(default=0,
        validators=[MaxValueValidator(3)])

    def days_until_due(self):
        if self.date_returned:
            return None
        else:
            return (self.due_date - datetime.date.today()).days

    def __str__(self):
        return '%s %s' % (self.book, self.start_date)


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reserve_date_time = models.DateTimeField(auto_now_add=True)
    open_reservation = models.BooleanField(default=True)

    def place_in_line(self):
        later_reservations = Reservation.objects.filter(
            book=self.book, reserve_date_time__lt=self.reserve_date_time)
        return len(later_reservations)

    def save(self, *args, **kwargs):
        if self.book.is_rented == True:
            if len(list(Reservation.objects.filter(
                user=self.user, book=self.book, open_reservation=True))) > 0:
                return
            else:
                super().save(*args, **kwargs) # Call the "real" save() method.
        else:
            return

    def __str__(self):
        return '%s %s' % (self.user, self.reserve_date)
