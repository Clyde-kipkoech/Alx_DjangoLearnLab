from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

from .models import Author, Book


class BookAPITests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        # Authenticated client
        self.auth_client = APIClient()
        self.auth_client.login(username="testuser", password="testpass123")

        # Sample author
        self.author = Author.objects.create(name="John Doe")

        # Sample books
        self.book1 = Book.objects.create(
            title="Book One", publication_year=2001, author=self.author
        )
        self.book2 = Book.objects.create(
            title="Book Two", publication_year=2005, author=self.author
        )

        # Endpoints
        self.list_url = reverse("book-list")      # /books/
        self.detail_url = reverse("book-detail", args=[self.book1.id])  # /books/<id>/

    # ---------- CRUD TESTS ----------

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Book One")

    def test_create_book_requires_auth(self):
        data = {
            "title": "New Book",
            "publication_year": 2020,
            "author": self.author.id,
        }
        # Unauthenticated
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated
        response = self.auth_client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book(self):
        data = {"title": "Updated Book", "publication_year": 2010, "author": self.author.id}
        response = self.auth_client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book")

    def test_delete_book(self):
        response = self.auth_client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # ---------- FILTERING, SEARCHING, ORDERING ----------

    def test_filter_books_by_publication_year(self):
        response = self.client.get(self.list_url, {"publication_year": 2001})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book One")

    def test_search_books_by_title(self):
        response = self.client.get(self.list_url, {"search": "Book Two"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book Two")

    def test_order_books_by_year(self):
        response = self.client.get(self.list_url, {"ordering": "publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years))


class PermissionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="pass123")
        self.author = Author.objects.create(name="Jane Doe")
        self.book = Book.objects.create(title="Test Book", publication_year=2015, author=self.author)
        self.detail_url = reverse("book-detail", args=[self.book.id])

    def test_unauthenticated_user_cannot_create_update_delete(self):
        # Create
        response = self.client.post(reverse("book-list"), {
            "title": "Blocked Book", "publication_year": 2022, "author": self.author.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Update
        response = self.client.put(self.detail_url, {
            "title": "Blocked Update", "publication_year": 2018, "author": self.author.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Delete
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
