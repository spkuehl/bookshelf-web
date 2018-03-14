from django.db import models
from books.models import Book
from bookshelf.users.models import User
from django.core.validators import MaxValueValidator


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=False, blank=False)
    renewel_count = models.PositiveIntegerField(default=0,
        validators=[MaxValueValidator(3)])

    def __str__(self):
        return '%s %s' % (self.book, self.start_date)