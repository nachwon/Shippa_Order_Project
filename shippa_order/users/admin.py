from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User, PointsLog


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('id', 'username', 'password')}),
        ("Personal Info", {'fields': ('email', 'first_name', 'last_name')}),
        ("Points", {'fields': ('points',)}),
        ("Authorizations", {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ("Logs", {'fields': ('last_login', 'date_joined')})
    )

    readonly_fields = ("id", "points")


class PointsLogAdmin(admin.ModelAdmin):
    list_display = ("user", "points_spent", "points_added", "points", "created_at")
    fieldsets = (
        (None, {"fields": ('user', "points_spent", "points_added", "points", "created_at")}),
    )
    list_filter = ("user", "created_at")
    readonly_fields = ("user", "points_spent", "points_added", "created_at")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser is True


admin.site.register(User, UserAdmin)
admin.site.register(PointsLog, PointsLogAdmin)
