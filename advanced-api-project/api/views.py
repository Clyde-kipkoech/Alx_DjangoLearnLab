from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from datetime import datetime
from .models import Book
from .serializers import BookSerializer



class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Permissions: read for everyone, write for authenticated users
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        title = serializer.validated_data.get("title")
        author = serializer.validated_data.get("author")

        if Book.objects.filter(title=title, author=author).exists():
            raise ValidationError("This author already has a book with the same title.")

        serializer.save()


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Permissions: read for everyone, write for authenticated users
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        pub_year = serializer.validated_data.get("publication_year")
        if pub_year and pub_year > datetime.now().year:
            raise ValidationError("Publication year cannot be in the future.")
        serializer.save()

