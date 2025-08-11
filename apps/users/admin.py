from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from ..accounts.models import Account


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'birth_date', 'kyc_status')}),
    )
    list_display = ('username', 'email', 'phone', 'kyc_status', 'is_staff')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')
    list_filter = ('type',)