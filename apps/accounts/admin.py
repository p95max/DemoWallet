from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'type', 'currency', 'created_at')
    list_filter = ('type', 'currency')
    search_fields = ('owner__username',)