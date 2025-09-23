from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class Author(models.Model):
    """
    Author model:
    Stores the name of the author.
    Each Author can have multiple Books (one-to-many relationship).
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model:
    Stores book details including title, publication year, 
    and links each book to a single Author.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
