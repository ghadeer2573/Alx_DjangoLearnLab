import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django-models.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Replace 'your_project_name' with your actual Django project folder name

# Sample Query 1: All books by a specific author
def books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author.name}: {[book.title for book in books]}")
    except Author.DoesNotExist:
        print(f"No author named {author_name} found.")


# Sample Query 2: List all books in a library
def books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library.name}: {[book.title for book in books]}")
    except Library.DoesNotExist:
        print(f"No library named {library_name} found.")


# Sample Query 3: Retrieve the librarian for a library
def librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)  # ✅ هذا هو السطر المطلوب
        print(f"Librarian for {library.name}: {librarian.name}")
    except Library.DoesNotExist:
        print(f"No library named {library_name} found.")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to library {library_name}.")



# You can test the functions like this:
if __name__ == "__main__":
    books_by_author("J.K. Rowling")
    books_in_library("Central Library")
    librarian_for_library("Central Library")
