from .models import Device, User
from django_rest_passwordreset.models import ResetPasswordToken


def get_device_by_id(*, mac_address: str) -> None or Device:
    try:
        return Device.objects.get(token=mac_address)
    except Device.DoesNotExist:
        pass


def get_user_from_token(token: str):
    try:
        token = ResetPasswordToken.object.get(key=token)
        
    except ResetPasswordToken.DoesNotExist:
        pass


