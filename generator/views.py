from rest_framework import viewsets, response, status
from .serializers import FileSerializer
from .services import create_shortened_link, get_file_obj_by_url, create_viewer, is_viewer_exist, get_viewer_obj
from django.shortcuts import redirect
from common.jwt import verify_member
from .models import Link
from common.qr import generate_qr
from common.ip import get_client_ip


class UserFileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    http_method_names = ['post', 'delete', 'get']
    queryset = Link.objects.all()

    def list(self, request, *args, **kwargs):
        member_id, error_response = verify_member(request)
        if error_response:
            return response.Response(error_response, status=status.HTTP_401_UNAUTHORIZED)
        request.data['member'] = member_id
        self.queryset = self.queryset.filter(member_id=member_id).order_by('-created_at')
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        member_id, error_response = verify_member(request)
        if error_response:
            return response.Response(error_response, status=status.HTTP_401_UNAUTHORIZED)
        request.data['member'] = member_id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            link = create_shortened_link(request)
            instance = serializer.save(link=link)
            instance.qr_code = generate_qr(request, instance)
            instance.save()
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
    try:
        analytics_obj = file_obj.link_analytics.get(link_id=file_obj.id)
        analytics_obj.no_of_clicks += 1
        ip_address = get_client_ip(request)
        viewer_obj = get_viewer_obj(ip_address)
        if not viewer_obj:
            analytics_obj.no_of_unique_viewers += 1
            viewer_instance = create_viewer(ip_address)
            analytics_obj.unique_viewers.add(viewer_instance.id)
        else:
            is_already_a_viewer = is_viewer_exist(viewer_obj, analytics_obj)
            if not is_already_a_viewer:
                analytics_obj.no_of_unique_viewers += 1
                analytics_obj.unique_viewers.add(viewer_obj.id)
        analytics_obj.save()
    except:
        pass

    if file_obj:
        return redirect(file_obj.file.url)
    return None
