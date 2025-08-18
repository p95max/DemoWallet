from rest_framework import serializers
from .models import Transfer

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = [
            'id', 'sender', 'receiver', 'amount', 'currency',
            'message', 'created_at', 'status'
        ]
        read_only_fields = ['id', 'created_at', 'status', 'sender']