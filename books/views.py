from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
import rentals


class BookViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('checkout', 'checkin', 'reservation', 'renew'):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminOrReadOnly]
        return [permission() for permission in permission_classes]

    @action(methods=['post', 'get'], detail=True)
    def checkout(self, request, pk=None):
        book = self.get_object()
        if book.is_rented:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            rental = book.create_rental(request.user)
            return Response(status=status.HTTP_201_CREATED)

    @action(methods=['post', 'get'], detail=True)
    def checkin(self, request, pk=None):
        book = self.get_object()
        if book.is_rented:
            book.finish_rental(request.user)
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post', 'get'], detail=True)
    def reservation(self, request, pk=None):
        book = self.get_object()
        if book.is_rented:
            reservation = book.create_reservation(request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post', 'get'], detail=True)
    def renew(self, request, pk=None):
        book = self.get_object()
        rental = rentals.models.Rental.objects.get(
                book=book, active_rental=True)
        if book.is_rented:
            if rental.renewel_count < 3:
                renew = book.renew_book(request.user)
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
