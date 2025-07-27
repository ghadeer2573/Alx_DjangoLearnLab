from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    # Your form logic to create a book
    pass

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Your edit logic
    pass

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Your delete logic
    pass

from django.shortcuts import render
from .models import Book
from .forms import BookSearchForm

def search_books(request):
    form = BookSearchForm(request.GET)
    results = []
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Book.objects.filter(title__icontains=query)
    return render(request, 'bookshelf/book_list.html', {'form': form, 'books': results})
