from rest_framework import serializers
from . import models


class CalculationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CalculationHistory
        fields = "__all__"