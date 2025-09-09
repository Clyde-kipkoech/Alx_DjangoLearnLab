from django.contrib import admin

# Register your models here.
from .models import Book

# Custom admin configuration
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")  # Show these fields in list view
    list_filter = ("publication_year", "author")            # Add filter sidebar
    search_fields = ("title", "author")                     # Enable search bar

# Register the Book model with the custom admin
admin.site.register(Book, BookAdmin)