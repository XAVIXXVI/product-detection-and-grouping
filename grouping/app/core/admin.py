"""
Django admin  customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BasUserAdmin

from core import models


class UserAdmin(BasUserAdmin):
    """Define the admin page for users."""
    ordering = ['id']
    list_display = ['email', 'name']


admin.site.register(models.User, UserAdmin)
