from django.db import models
import datetime

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

    def __str__(self):
        return self.title
