from django.contrib import admin

# Register your models here.
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book


# Custom admin configuration
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")  # Show these fields in list view
    list_filter = ("publication_year", "author")            # Add filter sidebar
    search_fields = ("title", "author")   


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "date_of_birth", "is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)

    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )


# Register models in Django admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book)# Enable search bar

# Register the Book model with the custom admin
admin.site.register(Book, BookAdmin)