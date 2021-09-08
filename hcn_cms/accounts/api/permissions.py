import re

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import SAFE_METHODS, BasePermission


class HasDeviceHeader(BasePermission):

    def has_permission(self, request, view):
        device_header = settings.HCN_SETTINGS['DEVICE_HEADER']
        api_prefixes = settings.DEVICE_HEADER_MIDDLEWARE['URL_PREFIX']
        excluded = '|'.join(settings.DEVICE_HEADER_MIDDLEWARE['EXCLUDE_ROUTES']).replace('/', '\\/')
        is_api_route = re.match(f"^/{api_prefixes}", request.path)

        if is_api_route and re.match(f"^((?!({excluded})).)*$", request.path) \
           and device_header in request.headers:
            if request.user and not isinstance(request.user, AnonymousUser):
                try:
                    next(filter(lambda device: device.get('id') == request.device.id, request.user.devices.values()))
                    return True
                except StopIteration:
                    pass
            else:
                return request.method in SAFE_METHODS
        return False
