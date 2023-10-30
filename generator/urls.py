from django.urls import path, include
from rest_framework import routers
from .views import UserFileViewSet

router = routers.DefaultRouter()
router.register(r'file', UserFileViewSet, basename="file-link-generator")

urlpatterns = [
    path('', include(router.urls)),
]