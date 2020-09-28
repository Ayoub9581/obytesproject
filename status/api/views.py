from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import StatusSerializer

from status.models import Status


class StatusListAPIView(generics.ListAPIView):
    serializer_class = StatusSerializer
    queryset = Status.objects.get_latest_messages()
