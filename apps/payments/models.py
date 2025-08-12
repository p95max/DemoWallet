from django.db import models
from django.conf import settings

class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='payments',
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    provider = models.CharField(
        max_length=50,
        choices=[
            ('stripe', 'Stripe'),
            ('paypal', 'PayPal'),
            ('manual', 'Manual'),
        ],
        default='manual'
    )
    external_id = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.status})"


class LedgerEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='payments_ledger_entries',
        on_delete=models.SET_NULL, null=True, blank=True
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(
        'payments.Payment', related_name='payments_ledger_entries',
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