from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    KYC_STATUS_CHOICES = [
        ('not_verified', 'Not Verified'),
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    kyc_status = models.CharField(max_length=20, choices=KYC_STATUS_CHOICES, default='not_verified')

    def __str__(self):
        return self.username