from rest_framework import serializers

from sliply.models import Slip


class SlipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slip
        fields = '__all__'