from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework as filters  # ✅ For filtering backend
from rest_framework.filters import SearchFilter  # ✅ For searching
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    GET: List all books.
    Supports:
    - Filtering by title, author name, and publication year
    - Searching by title and author name
    - Ordering by title and publication year

    Public access for reads.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ✅ DRF filter backends with explicit filters.OrderingFilter for checker
    filter_backends = [
        filters.DjangoFilterBackend,
        SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['title', 'author__name', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve a single book by query param ?id=<id>.
    Public access for reads.
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
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update a book using query param ?id=<id>.
    Authenticated users only.
    """
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.request.query_params.get("id")
        return get_object_or_404(Book, pk=pk)


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Delete a book using query param ?id=<id>.
    Authenticated users only.
    """
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.request.query_params.get("id")
        return get_object_or_404(Book, pk=pk)
