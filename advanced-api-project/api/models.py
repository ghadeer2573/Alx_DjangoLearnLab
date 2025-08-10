from django.db import models

# Author model represents a writer of one or more books
class Author(models.Model):
    name = models.CharField(max_length=255)  # Author's full name

    def __str__(self):
        return self.name


# Book model represents a single book written by an Author
class Book(models.Model):
    title = models.CharField(max_length=255)  # Title of the book
    publication_year = models.IntegerField()  # Year the book was published
    author = models.ForeignKey(
        Author, 
        related_name='books',  # Allows reverse lookup: author.books.all()
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
