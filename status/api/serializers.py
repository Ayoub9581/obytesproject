from django.utils.timesince import timesince
from rest_framework import serializers
from django.conf import settings
from status.models import Status
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    # user = UserSerializer(many=True, read_only=True,  required=False)
    owner = serializers.ReadOnlyField(source="user.email")
    class Meta:
        model = Status
        fields = ['message', 'created', 'owner']

