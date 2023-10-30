from django.db import models


# Create your models here.
class Member(models.Model):
    email = models.EmailField(max_length=255, null=True)
    password = models.CharField(max_length=16, null=True)
    username = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
