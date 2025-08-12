from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User



@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'birth_date', 'kyc_status')}),
    )
    list_display = ('username', 'email', 'phone_number', 'kyc_status', 'is_staff')
