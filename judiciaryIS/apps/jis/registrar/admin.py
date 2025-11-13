from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# We use UserAdmin to get the default, powerful admin interface for users
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Add 'role' to the fields shown in the admin list
    list_display = ['username', 'email', 'role', 'is_staff']
    # Add 'role' to the editable fields in the admin form
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
