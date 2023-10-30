from django.contrib import admin
from .models import Link


# Register your models here.
class LinkAdmin(admin.ModelAdmin):
    model = Link
    list_display = ['id', 'link', 'created_at', 'updated_at', 'file']
    readonly_fields = ['created_at', 'updated_at', 'file']


admin.site.register(Link, LinkAdmin)
