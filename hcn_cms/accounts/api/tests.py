from json import loads

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import Device

from .testing_utils import pre_register_device, pre_generate_access_token

# Create your tests here.


class AccountsTests(APITestCase):
    def test_device_registration(self):
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
            "consent": {
                "push_notification": True
            }
        }

        url = reverse('device-create')
        response = self.client.post(url, data=payload, format='json')
        content = loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(content['token'], 'token123')
        self.assertEqual(content['manufacturer'], 'Apple')

    @pre_register_device
    def test_user_registration(self, device_token):
        payload = {
            "email": "user1@email.com",
            "first_name": "User",
            "last_name": "User",
            "password": "password"
        }
        url = reverse('user-register')
        response = self.client.post(url, data=payload, HTTP_X_DEVICE_ID=device_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @pre_register_device
    def test_error_thrown_if_email_already_exists_during_registration(self, device_token):
        payload = {
            "email": "user1@email.com",
            "first_name": "User",
            "last_name": "User",
            "password": "password"
        }
        url = reverse('user-register')
        # First registration
        self.client.post(url, data=payload, HTTP_X_DEVICE_ID=device_token)

        # second registration attempt
        response = self.client.post(url, data=payload, HTTP_X_DEVICE_ID=device_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pre_generate_access_token
    @pre_register_device
    def test_error_thrown_if_user_does_not_own_device(self, device_token=None, access_token=None):
        device = Device.objects.get(token=device_token)
        device.user = None
        device.save()

        url = reverse('device-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}', HTTP_X_DEVICE_ID=device_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @pre_generate_access_token
    def test_we_cannot_make_request_without_device_header(self, access_token):
        url = reverse('device-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



