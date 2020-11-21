from rest_framework import serializers
from .models import StudioGhibli


class StudioGhibliSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioGhibli
        fields = '__all__'