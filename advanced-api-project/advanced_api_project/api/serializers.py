from rest_framework import serializers
from .models import Author, Book
from datetime import date


# BookSerializer is responsible for serializing and deserializing Book objects.
# It converts Book model instances into JSON and vice versa.
# Custom validation ensures publication_year cannot be in the future.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Custom field-level validation for publication_year.
    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# AuthorSerializer serializes Author objects.
# It includes a nested BookSerializer to show the author's related books.
# The relationship between Author and Book is handled through:
#   - The ForeignKey in the Book model (Book -> Author).
#   - The 'related_name="books"' on the ForeignKey.
# This allows us to include all books under an author in the JSON response.
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer: includes all books related to the author.
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        
        
        
        
