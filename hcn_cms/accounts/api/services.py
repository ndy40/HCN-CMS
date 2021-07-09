from typing import Dict

from accounts.models import Device, DeviceConsent


def create_device(*, data: Dict):
    device = Device.objects.create(**data)

    if 'consent' in data:
        consent = data['consent']
        consent.device = device
        consent.save()

    return device

