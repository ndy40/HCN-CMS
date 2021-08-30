from typing import List
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.api.testing_utils import pre_generate_access_token, pre_register_device, auth_login
from .models import Preacher, Series, Sermon

# Create your tests here.


class SermonsTestCase(APITestCase):
    @pre_register_device
    def setUp(self, device_token) -> None:
        super().setUp()
        login = auth_login(self, device_token=device_token)
        self._access_token = login['access']
        self._device_token = device_token

    def create_sermon(self):
        series_payload = {
            'title': 'title1',
            'description': 'description1',
            'tags': 'series1, series101'
        }
        series = Series.objects.create(**series_payload)
        preacher = Preacher.objects.create(name='Preacher1')
        sermon_payload = {
            'title': "title1",
            'series': series,
            'tags': ['series1']
        }
        sermons = Sermon.objects.create(**sermon_payload)
        sermons.preacher.add(preacher)

    def test_listing_all_series(self):
        series_payload = {
            'title': 'title1',
            'description': 'description1',
            'tags': 'series1, series101'
        }
        Series.objects.create(**series_payload)
        expected_response = {"id": 1, "title": "title1", "description": "description1", "starts_at": None,
                             "ends_at": None, "tags": ["series1", "series101"], "cover_image": None, "sermons": []}

        url = reverse('series-list')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Bearer {self._access_token}',
                                   HTTP_X_DEVICE_ID=self._device_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listing_of_sermons(self):
        self.create_sermon()
        url = reverse('sermon-lists')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Bearer {self._access_token}',
                                   HTTP_X_DEVICE_ID=self._device_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)

    def test_unauthenticated_user_cannot_add_like(self):
        self.create_sermon()

        url = reverse('sermon-lists')
        response = self.client.get(url, format='json', HTTP_X_DEVICE_ID=self._device_token)

        sermon_id = response.json()['results'][0]['@id']
        like_url = f'{sermon_id}add_like/'
        response = self.client.patch(like_url, format='json', HTTP_X_DEVICE_ID=self._device_token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_add_like(self):
        self.create_sermon()

        url = reverse('sermon-lists')
        response = self.client.get(url, format='json', HTTP_X_DEVICE_ID=self._device_token)

        sermon_id = response.json()['results'][0]['@id']
        like_url = f'{sermon_id}add_like/'
        response = self.client.patch(like_url, format='json', HTTP_X_DEVICE_ID=self._device_token,
                                     HTTP_AUTHORIZATION=f'Bearer {self._access_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authenticated_user_cannot_like_sermon_twice(self):
        self.create_sermon()

        url = reverse('sermon-lists')
        response = self.client.get(url, format='json', HTTP_X_DEVICE_ID=self._device_token)

        sermon_id = response.json()['results'][0]['@id']
        like_url = sermon_id + "add_like/"
        self.client.patch(like_url, format='json', HTTP_X_DEVICE_ID=self._device_token,
                          HTTP_AUTHORIZATION=f'Bearer {self._access_token}')
        response = self.client.patch(like_url, format='json', HTTP_X_DEVICE_ID=self._device_token,
                                     HTTP_AUTHORIZATION=f'Bearer {self._access_token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


