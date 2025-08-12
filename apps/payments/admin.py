from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'status', 'provider', 'created_at')
    list_filter = ('status', 'provider', 'created_at')
    search_fields = ('user__username', 'external_id')