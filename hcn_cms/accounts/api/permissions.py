from rest_framework.permissions import BasePermission
from django.conf import settings
import re


class HasDeviceHeader(BasePermission):

    def has_permission(self, request, view):
        device_header = settings.HCN_SETTINGS['DEVICE_HEADER']
        api_prefixes = settings.DEVICE_HEADER_MIDDLEWARE['URL_PREFIX']
        excluded = '|'.join(settings.DEVICE_HEADER_MIDDLEWARE['EXCLUDE_ROUTES']).replace('/', '\\/')
        is_api_route = re.match(f"^/{api_prefixes}", request.path)

        if is_api_route and re.match(f"^((?!({excluded})).)*$", request.path) \
               and device_header in request.headers:
            if request.user:
                try:
                    next(filter(lambda device: device.get('id') == request.device.id, request.user.devices.values()))
                    return True
                except StopIteration as e:
                    pass
            else:
                print('no user')
        return False
