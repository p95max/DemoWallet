from django.db import models
from django.conf import settings

class LedgerEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='ledger_entries',
        on_delete=models.SET_NULL, null=True, blank=True
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(
        'payments.Payment', related_name='ledger_entries',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    transaction = models.ForeignKey(
        'transactions.Transaction', related_name='ledger_entries',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    entry_type = models.CharField(
        max_length=20,
        choices=[
            ('credit', 'Credit'),
            ('debit', 'Debit'),
        ],
        default='credit'
    )

    def __str__(self):
        return f"{self.created_at} | {self.entry_type} | {self.amount} {self.currency}"

    class Meta:
        ordering = ['-created_at']