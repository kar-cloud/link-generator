from django.urls import path, include
from rest_framework import routers
from .views import RegisterMemberViewSet, LoginMemberViewSet

router = routers.DefaultRouter()
router.register(r'user/register', RegisterMemberViewSet, basename="register-user")
router.register(r'user/login', LoginMemberViewSet, basename="login-user")

urlpatterns = [
    path('', include(router.urls)),
]