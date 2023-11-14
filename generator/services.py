from accounts.services import get_member_details_by_id
from common.token_generator import generate_token
from generator.models import Link, Viewer


def create_shortened_link(request):
    domain_name = request.build_absolute_uri('/')
    member = get_member_details_by_id(request.data.get('member'))
    token = generate_token()
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
