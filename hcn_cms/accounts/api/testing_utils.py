from functools import wraps

from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Device, DeviceConsent, User


def pre_register_device(func):
    @wraps(func)
    def inner(*args, **kwargs):
        payload = {
            "token": "token123",
            "phone_model": "iPhone 11",
            "manufacturer": "Apple",
            "status": "ACTIVE",
            "os_name": "iOS",
            "os_version": "13.5",
            "wifi": True,
            "bluetooth": False,
            "screen_width": "0.536",
            "screen_height": "6.235",
        }

        device = Device.objects.create(**payload)
        DeviceConsent.objects.create(push_notification=True, device=device)
        func(device_token='token123', *args, **kwargs)

    return inner


def pre_generate_access_token(func):
    @wraps(func)
    def inner(*args, **kwargs):
        payload = {
            "email": "user1@email.com",
            "first_name": "User",
            "last_name": "User",
            "password": "password"
        }
        user = User.objects.create(**payload)
        refresh_token = RefreshToken.for_user(user)
        func(access_token=str(refresh_token.access_token), *args, **kwargs)

    return inner


def auth_login(self, device_token):
    payload = {
        "email": "user1@email.com",
        "first_name": "User",
        "last_name": "User",
        "password": "password"
    }
    url = reverse('user-register')
    self.client.post(url, data=payload, HTTP_X_DEVICE_ID=device_token)

    # get access token
    login_payload = {'username': 'user1@email.com', 'password': 'password'}
    response = self.client.post(reverse('token_obtain_pair'), data=login_payload, HTTP_X_DEVICE_ID=device_token)
    return response.json()
