from rest_framework import viewsets
from .models import Dispute
from .serializers import DisputeSerializer

class DisputeViewSet(viewsets.ModelViewSet):
    queryset = Dispute.objects.all()
    serializer_class = DisputeSerializer