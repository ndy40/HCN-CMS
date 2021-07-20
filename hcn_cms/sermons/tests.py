from typing import List
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.api.testing_utils import pre_generate_access_token, pre_register_device, auth_login
from .models import Series, Preacher, Sermon

# Create your tests here.


class SermonsTestCase(APITestCase):
    @pre_register_device
    def setUp(self, device_token) -> None:
        super().setUp()
        login = auth_login(self, device_token=device_token)
        self._access_token = login['access']
        self._device_token = device_token

    def test_listing_all_series(self):
        series_payload = {
            'title': 'title1',
            'description': 'description1',
            'tags': 'series1, series101'
        }
        Series.objects.create(**series_payload)
        expected_response = {"id": 1, "title": "title1", "description": "description1", "starts_at": None, \
                             "ends_at": None, "tags": ["series1", "series101"], "cover_image": None, "sermons": []}

        url = reverse('series-list')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Bearer {self._access_token}',
                                   HTTP_X_DEVICE_ID=self._device_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        assert expected_response in response.json()['results']

    def test_listing_of_sermons(self):
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

        url = reverse('sermon-lists')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Bearer {self._access_token}',
                                   HTTP_X_DEVICE_ID=self._device_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)

