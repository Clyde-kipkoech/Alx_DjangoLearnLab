from django.db import models

# The Author model represents a writer who can have multiple books.
# Fields:
#   - name: stores the author's name (string, max 255 characters).
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# The Book model represents a book written by an Author.
# Fields:
#   - title: the title of the book.
#   - publication_year: year when the book was published.
#   - author: foreign key to Author, establishing a one-to-many relationship.
#     One Author can have many Books, but each Book belongs to one Author.
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        related_name="books",  # allows reverse lookup: author.books.all()
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
