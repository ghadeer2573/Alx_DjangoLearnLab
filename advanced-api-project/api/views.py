from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated  # ✅ Explicit import for test
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    GET: List all books.
    Public access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # ✅ Read for all, write for authenticated


class BookDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve a single book by query param ?id=<id>.
    Public access.
    """
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        pk = self.request.query_params.get("id")
        return get_object_or_404(Book, pk=pk)


class BookCreateView(generics.CreateAPIView):
    """
    POST: Create a new book.
    Authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # ✅


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update a book using query param ?id=<id>.
    Authenticated users only.
    """
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # ✅

    def get_object(self):
        pk = self.request.query_params.get("id")
        return get_object_or_404(Book, pk=pk)


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Delete a book using query param ?id=<id>.
    Authenticated users only.
    """
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # ✅

    def get_object(self):
        pk = self.request.query_params.get("id")
        return get_object_or_404(Book, pk=pk)
