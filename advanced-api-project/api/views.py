from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from datetime import datetime
from .models import Book
from .serializers import BookSerializer

"""
Custom views for the Book model using DRF generic views.
Each view handles a specific CRUD operation.
"""

# GET /api/books/ → list all books
class ListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public access


# GET /api/books/<id>/ → retrieve one book
class DetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public access


# POST /api/books/ → create a book
class CreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can create

    def perform_create(self, serializer):
        title = serializer.validated_data.get("title")
        author = serializer.validated_data.get("author")
        if Book.objects.filter(title=title, author=author).exists():
            raise ValidationError("This author already has a book with the same title.")
        serializer.save()


# PUT/PATCH /api/books/<id>/ → update a book
class UpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can update

    def perform_update(self, serializer):
        pub_year = serializer.validated_data.get("publication_year")
        if pub_year and pub_year > datetime.now().year:
            raise ValidationError("Publication year cannot be in the future.")
        serializer.save()


# DELETE /api/books/<id>/ → delete a book
class DeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can delete
