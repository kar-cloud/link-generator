import jwt
from datetime import datetime, timedelta
from django.conf import settings


def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')


def decode_token(token):
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
    except:
        return None


def verify_member(request):
    if not request.META.get('HTTP_AUTHORIZATION'):
        return None, {"error": "Authorization Header Missing"}
    split_token = request.META['HTTP_AUTHORIZATION'].split(' ')
    if not len(split_token) == 2:
        return None, {"error": "Invalid Token"}
    token = split_token[1]
    token_details = decode_token(token)
    if token_details:
        return token_details.get('user_id'), None
    return None, {"error": "Invalid Token"}
