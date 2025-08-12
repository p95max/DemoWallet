from django.db import models
from django.conf import settings

class Dispute(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('under_review', 'Under Review'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='disputes',
        on_delete=models.CASCADE
    )
    payment = models.ForeignKey(
        'payments.Payment', related_name='disputes',
        on_delete=models.CASCADE
    )
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_comment = models.TextField(blank=True)

    def __str__(self):
        return f"Dispute #{self.id} by {self.user} for payment {self.payment.id} ({self.status})"