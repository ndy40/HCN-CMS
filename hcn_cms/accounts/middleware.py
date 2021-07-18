import re

from django.core.cache import cache
from django.utils.functional import SimpleLazyObject
from django.conf import settings
from django.http.response import HttpResponseForbidden

from .selectors import get_device_by_id


def get_device(request):
    # check the cache first before hitting the db and caching
    device_id = request.headers.get(settings.HCN_SETTINGS['DEVICE_HEADER'])

    cached_device = cache.get(f'hcn-device-header-{device_id}')

    if cached_device:
        return cached_device

    device = get_device_by_id(mac_address=device_id)

    if device:
        request.device = device

    return device


class ResolveDeviceMiddlware(object):
    """
    Each API Request can provide the `x-hcn-deviceId` header. This will be used to resolve the associated user device
    for this call. The value should also be cached and assigned to request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        device_header = settings.HCN_SETTINGS['DEVICE_HEADER']
        if device_header in request.headers:
            device_id = request.headers.get(device_header)

            if device_id:
                request.device = SimpleLazyObject(lambda: get_device(request))

        return self.get_response(request)
