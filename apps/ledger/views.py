from .models import LedgerEntry
from .serializers import LedgerEntrySerializer
from rest_framework import viewsets

class LedgerEntryViewSet(viewsets.ModelViewSet):
    queryset = LedgerEntry.objects.all()
    serializer_class = LedgerEntrySerializer