# bookshelf/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django import forms
from .models import Book
from .forms import ExampleForm


# ------------------------------
# Secure Form for Books
# ------------------------------
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]


# ------------------------------
# Views with Secure Handling
# ------------------------------

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """List all books (protected by can_view)."""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    """Add a new book (protected by can_create)."""
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():  # ✅ input validated and sanitized
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "bookshelf/form_example.html", {"form": form, "action": "Add"})


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    """Edit an existing book (protected by can_edit)."""
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():  # ✅ validation before saving
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "bookshelf/form_example.html", {"form": form, "action": "Edit"})


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    """Delete a book (protected by can_delete)."""
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "bookshelf/confirm_delete.html", {"book": book})

def example_form_view(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")  # assumes you have a book_list view
    else:
        form = ExampleForm()
    return render(request, "form_example.html", {"form": form})
