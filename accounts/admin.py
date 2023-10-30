from django.contrib import admin
from accounts.models import Member


# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    model = Member
    list_display = ['id', 'email', 'password', 'username', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Member, MemberAdmin)
