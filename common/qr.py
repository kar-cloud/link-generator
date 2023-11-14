import qrcode
import os
from accounts.services import get_member_details_by_id

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = '{}/media/qr/'.format(BASE_DIR)

def generate_qr(request, instance):
     if not os.path.exists(PATH):
          os.makedirs(PATH)
     domain_name = request.build_absolute_uri('/')
     file_name = instance.link.split("/")[-1] + ".png"
     image = qrcode.make(instance.link)
     image.save(PATH + file_name)
     return domain_name + "media/qr/" + file_name
