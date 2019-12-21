from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ("Personal Info", {'fields': ('email', 'first_name', 'last_name')}),
        ("Authorizations", {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ("Logs", {'fields': ('last_login', 'date_joined')})
    )


admin.site.register(User, UserAdmin)
