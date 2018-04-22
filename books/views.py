from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework import viewsets
from rest_framework.decorators import action
import rentals

class BookViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(methods=['post'], detail=True, permission_classes=[])
    def checkout(self, request, pk=None):

        book = self.get_object()

        rental = book.create_rental(request.user)

        return rental
