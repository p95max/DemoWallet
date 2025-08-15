from django.db import models
from apps.accounts.models import Account

class Transaction(models.Model):
    TXN_TYPE_CHOICES = [
        ('p2p', 'P2P Transfer'),
        ('topup', 'Top-up'),
        ('payment', 'Payment'),
        ('refund', 'Refund'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    account_from = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='outgoing_transactions', null=True, blank=True)
    account_to = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='incoming_transactions', null=True, blank=True)
    txn_type = models.CharField(max_length=20, choices=TXN_TYPE_CHOICES, default='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='EUR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    idempotency_key = models.CharField(max_length=128, null=True, blank=True, unique=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.txn_type}: {self.amount} {self.currency} ({self.status})"