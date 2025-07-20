from django.urls import path
from . import views

urlpatterns = [
    path("add_book/", views.add_book, name="add_book"),
    path("edit_book/<int:pk>/", views.edit_book, name="edit_book"),
    path("delete_book/<int:pk>/", views.delete_book, name="delete_book"),

    # Role-based views if required in your project
    path("admin_view/", views.admin_view, name="admin_view"),
    path("librarian_view/", views.librarian_view, name="librarian_view"),
    path("member_view/", views.member_view, name="member_view"),

    # Auth views
    path("register/", views.register, name="register"),
    path("login/", views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", views.LogoutView.as_view(template_name="logout.html"), name="logout"),
]
