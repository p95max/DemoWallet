from django.db import models
from django.conf import settings
from apps.accounts.models import Account

class Transfer(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sent_transfers', on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='received_transfers', on_delete=models.CASCADE
    )
    from_account = models.ForeignKey(
        Account, related_name='outgoing_transfers', on_delete=models.CASCADE
    )
    to_account = models.ForeignKey(
        Account, related_name='incoming_transfers', on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8)
    message = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=16,
        choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')],
        default='pending'
    )

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.amount} {self.currency}"