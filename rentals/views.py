from .models import Rental
from .serializers import RentalSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework import viewsets


class RentalViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Books.
    """
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAdminOrReadOnly]
