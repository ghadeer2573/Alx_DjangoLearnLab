from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import login
from .models import User
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

# Register new user
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"user": UserSerializer(user).data, "token": token.key})

# Login
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"user": UserSerializer(user).data, "token": token.key})

# User Profile
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

# accounts/views.py
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import PublicUserSerializer

User = get_user_model()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    target = generics.get_object_or_404(User, pk=user_id)
    if target == request.user:
        return Response({"detail": "Cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
    request.user.follow(target)
    return Response({"detail": f"You are now following {target.username}."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    target = generics.get_object_or_404(User, pk=user_id)
    if target == request.user:
        return Response({"detail": "Cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
    request.user.unfollow(target)
    return Response({"detail": f"You have unfollowed {target.username}."}, status=status.HTTP_200_OK)

# Optional: list followers or following for a user
class FollowersListView(generics.ListAPIView):
    serializer_class = PublicUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = generics.get_object_or_404(User, pk=user_id)
        return user.followers.all()

class FollowingListView(generics.ListAPIView):
    serializer_class = PublicUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = generics.get_object_or_404(User, pk=user_id)
        return user.following.all()
