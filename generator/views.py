from rest_framework import viewsets, response, status
from .serializers import FileSerializer
from .services import create_shortened_link, get_file_obj_by_url
from django.shortcuts import redirect
from common.jwt import verify_member
from .models import Link


class UserFileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    http_method_names = ['post', 'delete']
    queryset = Link.objects.all()

    def create(self, request, *args, **kwargs):
        member_id, error_response = verify_member(request)
        if error_response:
            return response.Response(error_response, status=status.HTTP_401_UNAUTHORIZED)
        request.data['member'] = member_id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            link = create_shortened_link(request)
            serializer.save(link=link)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        member_id, error_response = verify_member(request)
        if error_response:
            return response.Response(error_response, status=status.HTTP_401_UNAUTHORIZED)
        instance = self.get_object()
        if not instance:
            return response.Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        if instance.member.id != member_id:
            return response.Response({"error": "UnAuthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(self, request, *args, **kwargs)


def get_file_view(request, **kwargs):
    username = kwargs.get('username')
    token = kwargs.get('token')
    domain_name = request.build_absolute_uri('/')
    url = '{0}{1}/{2}'.format(domain_name, username, token)
    file_obj = get_file_obj_by_url(url)
    if file_obj:
        return redirect(file_obj.file.url)
    return None
