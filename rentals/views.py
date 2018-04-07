from .models import Rental, Reservation
from .serializers import RentalSerializer, ReservationSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework import viewsets


class RentalViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Rentals.
    """
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Reservations.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
