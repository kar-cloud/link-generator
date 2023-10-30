from accounts.services import get_member_details_by_id
from common.token_generator import generate_token
from generator.models import Link


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
