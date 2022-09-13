from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from forum_comments.models import OrganizationModel, UserModel


@admin.register(UserModel)
class CustomAdminUser(UserAdmin):
    fieldsets = (
        (None, {"fields": ("organization", "username", "email", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {"fields": ("email", "username", "password1", "password2")},
        ),
    )
    list_display = ("username", "email", "organization", "is_active")
    list_filter = ["is_active", "organization"]
    search_fields = ["email", "organization__name", "organization__NIP"]

    class Meta:
        abstract = True


@admin.register(OrganizationModel)
class CustomOrganizationAdmin(admin.ModelAdmin):
    fields = ("name", "NIP", "country", "domain_name")
    list_display = ("name", "NIP", "country", "domain_name")
    list_filter = ["country"]
    search_fields = ["name", "NIP"]
