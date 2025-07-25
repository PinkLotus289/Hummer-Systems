from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'phone_number',
        'invite_code',
        'used_invite_code',
        'activated_by',
        'is_staff',
        'is_active',
    )
    search_fields = ('phone_number', 'invite_code', 'used_invite_code')
    list_filter = ('is_staff', 'is_active')

