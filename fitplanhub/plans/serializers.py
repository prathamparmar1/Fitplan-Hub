from rest_framework import serializers
from .models import FitnessPlan

class FitnessPlanSerializer(serializers.ModelSerializer):
    trainer_name = serializers.CharField(
        source='trainer.name',
        read_only=True
    )

    class Meta:
        model = FitnessPlan
        fields = [
            'id',
            'title',
            'description',
            'price',
            'duration_days',
            'trainer_name',
            'created_at'
        ]
