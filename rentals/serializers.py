from rest_framework import serializers
from .models import Rental, Reservation


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ('id', 'user', 'book', 'start_date',
                  'due_date', 'date_returned', 'renewel_count')


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'user', 'book')
