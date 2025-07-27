from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book, Library, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView

# Task 1: Views
@login_required
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Task 2: Authentication
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Task 3: Role-Based Access Control

def check_role(role):
    def inner(user):
        return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == role
    return user_passes_test(inner)

@check_role('Admin')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@check_role('Librarian')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@check_role('Member')
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# Task 4: Permissions
@permission_required('relationship_app.can_add_book')
def add_book(request):
    return render(request, 'relationship_app/secure_action.html', {'action': 'Add Book'})

@permission_required('relationship_app.can_change_book')
def edit_book(request):
    return render(request, 'relationship_app/secure_action.html', {'action': 'Edit Book'})

@permission_required('relationship_app.can_delete_book')
def delete_book(request):
    return render(request, 'relationship_app/secure_action.html', {'action': 'Delete Book'})