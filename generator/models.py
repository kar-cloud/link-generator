from django.db import models
from accounts.models import Member


# Create your models here
class Link(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="link_host")
    file = models.FileField(upload_to="files")
    description = models.TextField(max_length=1000, verbose_name="Link Description")
    link = models.URLField(max_length=300, verbose_name="Link URL", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
