from django.urls import path, include
from rest_framework import routers
from .views import RegisterMemberViewSet, LoginMemberViewSet, VerifyMemberViewSet, get_user_details

router = routers.DefaultRouter()
router.register(r'user/register', RegisterMemberViewSet, basename="register-user")
router.register(r'user/login', LoginMemberViewSet, basename="login-user")
router.register(r'user/verify', VerifyMemberViewSet, basename="login-user")

urlpatterns = [
    path('', include(router.urls)),
    path('user/', get_user_details, name="get_user_details")
]
