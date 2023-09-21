from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreationForm
from accounts.models import AccountTier, User


class CustomUserAccountAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User
    list_display = [
        "username",
        "account_tier",
        "email",
    ]
    list_display_links = ["username"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("account_tier",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("account_tier",)}),)


admin.site.register(User, CustomUserAccountAdmin)
admin.site.register(AccountTier)
