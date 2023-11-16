from rest_framework import viewsets, response, status
from rest_framework.decorators import api_view
from .serializers import MemberSerializer
from .services import get_member_details, get_member_details_by_id
from common.jwt import generate_token, verify_member


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
            if request.data.get('password') != member_obj.password:
                return response.Response({"error": "Invalid Email or Password"}, status=status.HTTP_400_BAD_REQUEST)
            jwt_token = generate_token(member_obj.id)
            return response.Response({"token": jwt_token}, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyMemberViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        user_id, error = verify_member(request)
        if user_id and not error:
            return response.Response({"user": "Verified"}, status=status.HTTP_200_OK)
        return response.Response({"user": "Not Verified"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_details(request):
    member_id, error_response = verify_member(request)
    if error_response:
        return response.Response(error_response, status=status.HTTP_401_UNAUTHORIZED)

    member_obj = get_member_details_by_id(member_id)
    if member_obj:
        return response.Response({
            "email": member_obj.email,
            "username": member_obj.username
        }, status=status.HTTP_200_OK)
    return response.Response({}, status=status.HTTP_400_BAD_REQUEST)
