from django.urls import path
from .views import (
    list_books,
    LibraryDetailView,
    CustomLoginView,
    CustomLogoutView,
    RegisterView,
    admin_view,
    librarian_view,
    member_view
)

urlpatterns = [
    # قائمة الكتب (function-based view)
    path('books/', list_books, name='list_books'),

    # تفاصيل المكتبة (class-based view)
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # تسجيل الدخول والخروج والتسجيل
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # صفحات خاصة بالأدوار (admin / librarian / member)
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),
]
