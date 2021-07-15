from typing import Dict

from accounts.models import Device, DeviceConsent, User


def create_device(*, data: Dict):
    device = Device.objects.create(**data)

    if 'consent' in data:
        consent = data['consent']
        consent.device = device
        consent.save()

    return device


def _does_email_exists(email: str):
    try:
        User.objects.get(email=email)
    except User.DoesNotExist:
        return False
    return True


def create_user(*, data: Dict):
    if _does_email_exists(data['email']) :
        raise ValueError('User email already exists')
    user = User.objects.create(**data)
    return user


def attach_device_to_user(user_id: int, device: Device):
    user = User.objects.get(pk=user_id)
    user.devices.add(device)
    user.save()
