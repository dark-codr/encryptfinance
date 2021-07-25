from __future__ import absolute_import

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from encryptfinance.users.forms import (
    UserChangeForm,
    UserCreationForm,
    UserProfileForm,
    UserVerifyForm,
)
from encryptfinance.users.models import Testimonial, UserProfile, UserVerify

from ..utils.export_as_csv import ExportCsvMixin

User = get_user_model()

admin.site.register(Testimonial)
admin.site.register(UserProfile)
admin.site.register(UserVerify)


class UserProfile(admin.StackedInline):
    form = UserProfileForm
    model = UserProfile

    def __init__(self, parent_model, admin_site):
        self.fk_name = getattr(self.model, 'fk_name', None)
        super().__init__(parent_model, admin_site)


class UserVerify(admin.StackedInline):
    form = UserVerifyForm
    model = UserVerify
   
@admin.register(User)
class UserAdmin(auth_admin.UserAdmin, ExportCsvMixin):

    form = UserChangeForm
    add_form = UserCreationForm
    list_per_page = 250
    inlines = [UserProfile, UserVerify]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "middle_name", "last_name", "email")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    # "groups",
                    # "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("deposit_date", "last_login", "date_joined")}),
    )
    list_display = [
        "__str__",
        "balance",
        "plan",
        "rate",
        "days",
        "unique_id",
        "deposit_date",
        "withdrawal_date",
        "can_withdraw",
        "has_deposited",
        "is_verified",
        "is_active",
        "is_superuser",
        "last_login",
        "date_joined",
    ]
    list_editable = [
        "balance",
        "has_deposited",
        "is_verified",
        "is_active",
        "is_superuser",
    ]
    empty_value_display = '-empty-'
    search_fields = ["__str__"]

    actions = [
        "export_as_csv",
    ]

    def can_withdraw(self, obj):
        withdraw = obj.can_withdraw()
        if withdraw:
            return format_html("<input type='checkbox' checked>")
        else:
            return format_html("<input type='checkbox'>")
        