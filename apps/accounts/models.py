from django.db import models
from django.conf import settings

class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('wallet', 'Wallet'),
        ('company', 'Company/Provider'),
    ]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts')
    type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='wallet')
    currency = models.CharField(max_length=3, default='EUR')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'type', 'currency')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.owner} {self.type} ({self.currency})'