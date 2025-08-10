from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# ListView: Retrieve all books (Read-only for everyone)
class BookListView(generics.ListAPIView):
    """
    GET: List all books.
    Read-only for unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can read


# DetailView: Retrieve single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve a single book by ID.
    Read-only for unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can read


# CreateView: Add a new book
class BookCreateView(generics.CreateAPIView):
    """
    POST: Create a new book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
       
    def perform_create(self, serializer):
        # Example: Ensure author is set to a specific default if missing
        if 'author' not in self.request.data:
            from .models import Author
            default_author, _ = Author.objects.get_or_create(name="Unknown Author")
            serializer.save(author=default_author)
        else:
            serializer.save()  # Only authenticated users


# UpdateView: Modify existing book
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update an existing book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# DeleteView: Remove a book
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Delete a book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
