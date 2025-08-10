from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username="user1", password="pass1234")
        self.other_user = User.objects.create_user(username="user2", password="pass5678")

        # Create books
        self.book1 = Book.objects.create(
            title="Book One", author="Author A", publication_year=2020
        )
        self.book2 = Book.objects.create(
            title="Book Two", author="Author B", publication_year=2021
        )

        # URL patterns (must match names in api/urls.py)
        self.list_url = reverse("book-list")
        self.create_url = reverse("book-create")
        self.update_url = reverse("book-update", args=[self.book1.id])
        self.delete_url = reverse("book-delete", args=[self.book2.id])
        self.detail_url = reverse("book-detail", args=[self.book1.id])

    def test_list_books_public(self):
        """Anyone can list books."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book_authenticated(self):
        """Authenticated user can create a book."""
        self.client.login(username="user1", password="pass1234")
        data = {
            "title": "New Book",
            "author": "Author C",
            "publication_year": 2022
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        """Unauthenticated users cannot create books."""
        data = {
            "title": "Unauthorized Book",
            "author": "Author D",
            "publication_year": 2023
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        """Authenticated user can update a book."""
        self.client.login(username="user1", password="pass1234")
        data = {"title": "Updated Book One"}
        response = self.client.patch(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book One")

    def test_update_book_unauthenticated(self):
        """Unauthenticated user cannot update a book."""
        data = {"title": "Hacker Edit"}
        response = self.client.patch(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authenticated(self):
        """Authenticated user can delete a book."""
        self.client.login(username="user1", password="pass1234")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_book_unauthenticated(self):
        """Unauthenticated user cannot delete a book."""
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_books_by_title(self):
        """Can filter books by title."""
        response = self.client.get(self.list_url, {"title": "Book One"})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book One")

    def test_search_books_by_author(self):
        """Can search books by author."""
        response = self.client.get(self.list_url, {"search": "Author B"})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["author"], "Author B")

    def test_order_books_by_publication_year(self):
        """Can order books by publication year."""
        response = self.client.get(self.list_url, {"ordering": "publication_year"})
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years))
