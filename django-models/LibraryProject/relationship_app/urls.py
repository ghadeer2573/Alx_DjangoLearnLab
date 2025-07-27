from django.urls import path
from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register_view, name='register'),

    path('admin_only/', views.admin_view, name='admin_view'),
    path('librarian_only/', views.librarian_view, name='librarian_view'),
    path('member_only/', views.member_view, name='member_view'),

    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/', views.edit_book, name='edit_book'),
    path('delete_book/', views.delete_book, name='delete_book'),
]