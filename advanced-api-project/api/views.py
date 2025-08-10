from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    GET: List all books with filtering, searching, and ordering.
    - Filtering: title, author name, publication_year
    - Searching: title, author name
    - Ordering: title, publication_year
    Public access for reading.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ✅ Enable filtering, searching, ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    # Filtering fields (exact match by default)
    filterset_fields = {
        'title': ['exact', 'icontains'],
        'author__name': ['exact', 'icontains'],
        'publication_year': ['exact', 'gte', 'lte'],
    }

    # Search fields (partial match)
    search_fields = ['title', 'author__name']

    # Ordering fields
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering

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
