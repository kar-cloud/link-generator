from accounts.models import Member
from django.db.models import Q


def get_member_details_by_id(member_id):
    try:
        return Member.objects.get(id=member_id)
    except:
        return None


def get_member_details(username=None, email=None):
    try:
        return Member.objects.get(Q(username=username) | Q(email=email))
    except:
        return None


