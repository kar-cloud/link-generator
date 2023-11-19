from accounts.services import get_member_details_by_id
from common.token_generator import generate_token
from generator.models import Link, Viewer


def create_shortened_link(request, member_id):
    domain_name = request.build_absolute_uri('/')
    member = get_member_details_by_id(member_id)
    custom_url = request.data.get('custom_url')
    is_valid_custom_url = False
    if custom_url is not None:
        links = get_link_objects_by_member_id(member.id, custom_url=custom_url)
        if not links:
            is_valid_custom_url = True
    token = custom_url if is_valid_custom_url else generate_token()
    return '{0}{1}/{2}'.format(domain_name, member.username, token)


def get_file_obj_by_url(url):
    try:
        return Link.objects.get(link=url)
    except:
        return None


def create_viewer(ip_address):
    instance = Viewer.objects.create(ip_address=ip_address)
    return instance


def is_viewer_exist(viewer_obj, analytics_obj):
    try:
        if analytics_obj.unique_viewers.filter(id=viewer_obj.id).exists():
            return True
        return False
    except:
        return False


def get_viewer_obj(ip_address):
    try:
        return Viewer.objects.get(ip_address=ip_address)
    except:
        return None
    

def get_link_objects_by_member_id(member_id, **kwargs):
    return Link.objects.filter(member_id=member_id, **kwargs)
