from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

User = get_user_model()


class CustomUserAdmin(DefaultUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)


try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)
