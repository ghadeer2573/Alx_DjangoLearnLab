from django.urls import path
from .views import RegisterView, LoginView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]

from django.urls import path
from . import views

urlpatterns = [
    # existing routes: register/login/profile...
    path('follow/<int:user_id>/', views.follow_user, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow'),
    path('<int:user_id>/followers/', views.FollowersListView.as_view(), name='followers-list'),
    path('<int:user_id>/following/', views.FollowingListView.as_view(), name='following-list'),
]
