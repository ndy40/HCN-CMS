from .models import Device


def get_device_by_id(*, mac_address: str) -> None or Device:
    try:
        return Device.objects.get(token=mac_address)
    except Device.DoesNotExist:
        pass
