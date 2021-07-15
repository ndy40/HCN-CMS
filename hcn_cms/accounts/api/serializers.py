from datetime import datetime, timezone

import rest_framework.exceptions
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse
from rest_framework import serializers

from accounts.models import Device, DeviceConsent, User
from .services import create_device, create_user


class DeviceConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceConsent
        fields = ['push_notification']

    def to_internal_value(self, data):
        return DeviceConsent(**dict(data))


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    consent = DeviceConsentSerializer()

    class Meta:
        model = Device
        fields = '__all__'

    def create(self, validated_data):
        return create_device(data=validated_data)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class RegisterUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    devices = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='device-detail')

    def create(self, validated_data):
        try:
            validated_data['is_active'] = True
            validated_data['date_joined'] = datetime.now(tz=timezone.utc)
            validated_data['password'] = make_password(validated_data['password'])
            validated_data['username'] = validated_data['email']
            return create_user(data=validated_data)
        except ValueError as e:
            raise ValidationError(detail={"message": e})


class UserSerializer(serializers.HyperlinkedModelSerializer):
    devices = serializers.HyperlinkedRelatedField(many=True, view_name='device-detail', read_only=True)

    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions', 'is_staff', 'is_superuser']
