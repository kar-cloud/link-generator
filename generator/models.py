from django.db import models
from accounts.models import Member


class Link(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="link_host")
    file = models.FileField(upload_to="files", null=True, blank=True)
    description = models.TextField(max_length=1000, verbose_name="Link Description", null=True, blank=True)
    link = models.URLField(max_length=300, verbose_name="Link URL", null=True, blank=True)
    qr_code = models.URLField(max_length=300, verbose_name="QR Code", null=True, blank=True)
    custom_url = models.CharField(max_length=30, verbose_name="Custom URL Name", null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)


class Viewer(models.Model):
    ip_address = models.CharField(max_length=20, verbose_name="IP Address")


class Analytics(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name="link_analytics")
    no_of_clicks = models.IntegerField(default=0)
    no_of_unique_viewers = models.IntegerField(default=0)
    unique_viewers = models.ManyToManyField(Viewer, related_name="viewer")
