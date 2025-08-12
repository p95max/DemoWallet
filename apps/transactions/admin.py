from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'txn_type', 'amount', 'currency', 'status', 'account_from', 'account_to', 'created_at')
    list_filter = ('txn_type', 'status', 'currency')
    search_fields = ('idempotency_key',)