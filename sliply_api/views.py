from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics

from sliply.models import Slip
from .serializers import SlipSerializer


class SlipListViewAPI(LoginRequiredMixin, generics.ListCreateAPIView):
    serializer_class = SlipSerializer

    def get_queryset(self):
        return Slip.objects.filter(owner=self.request.user)

