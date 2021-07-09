from rest_framework import serializers
from accounts.models import Device, DeviceConsent
from .services import create_device


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

