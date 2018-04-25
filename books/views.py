from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
import rentals


class BookViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(methods=['post', 'get'], detail=True)
    def checkout(self, request, pk=None):
        book = self.get_object()
        if book.is_rented:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            rental = book.create_rental(request.user)
            return Response(status=status.HTTP_201_CREATED)
