from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = get_user_model()
        fields = ('username','password',)
