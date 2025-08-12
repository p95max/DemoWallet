from django.contrib import admin

from .models import LedgerEntry

@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'currency', 'entry_type', 'created_at', 'payment', 'transaction')
    list_filter = ('entry_type', 'currency', 'created_at')
    search_fields = ('user__username', 'description')