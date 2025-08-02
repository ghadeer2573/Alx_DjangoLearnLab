from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

# Already defined: BookList (for list view)
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# New ViewSet: handles full CRUD
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
