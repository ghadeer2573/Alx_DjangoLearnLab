from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet

router = DefaultRouter()
router.register(r"notifications", NotificationViewSet, basename="notifications")

urlpatterns = router.urls
from django.urls import path, include

urlpatterns = [
    path("api/", include("posts.urls")),
    path("api/", include("notifications.urls")),
]
