from django.db import models
from django.conf import settings

class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('wallet', 'Wallet'),
        ('company', 'Company/Provider'),
    ]

    CURRENCY_TYPE_CHOICES = [
        ('usd', 'USD'),
        ('eur', 'EUR'),
    ]


    name = models.CharField(max_length=50, default='Wallet')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='wallet')
    currency = models.CharField(max_length=3, choices=CURRENCY_TYPE_CHOICES, default='EUR')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def balance(self):
        return sum(tx.amount for tx in self.transactions.all())

    class Meta:
        unique_together = ('owner', 'type', 'currency')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.owner} {self.type} ({self.currency})'