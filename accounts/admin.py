from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import DashboardUser


@admin.register(DashboardUser)
class DashboardUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets
