from django.contrib import admin
from .models import Rental


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    pass
