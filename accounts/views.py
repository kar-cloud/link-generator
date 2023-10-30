from rest_framework import viewsets, response, status
from .serializers import MemberSerializer
from .services import get_member_details
from common.jwt import generate_token


# Create your views here.
class RegisterMemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            member_obj = get_member_details(request.data.get('username'), request.data.get('email'))
            if member_obj:
                return response.Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
            member_obj = serializer.save()
            jwt_token = generate_token(member_obj.id)
            return response.Response({"token": jwt_token}, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginMemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            member_obj = get_member_details(None, request.data.get('email'))
            if not member_obj:
                return response.Response({"error": "Invalid Email or Password"}, status=status.HTTP_400_BAD_REQUEST)
            jwt_token = generate_token(member_obj.id)
            return response.Response({"token": jwt_token}, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
