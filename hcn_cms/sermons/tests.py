from typing import List
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.api.testing_utils import pre_generate_access_token, pre_register_device, auth_login
from .models import Preacher, Series, Sermon

# Create your tests here.


def create_series():
    series_payload = {
        'title': 'title1',
        'description': 'description1',
        'tags': 'series1, series101'
    }
    Series.objects.create(**series_payload)


class TestSetupMixin:
    @pre_register_device
    def setUp(self, device_token) -> None:
        super().setUp()
        login = auth_login(self, device_token=device_token)
        self._access_token = login['access']
        self._device_token = device_token


def create_sermon():
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


class SermonsTestCase(TestSetupMixin, APITestCase):

    def test_listing_all_series(self):
        series_payload = {
            'title': 'title1',
            'description': 'description1',
            'tags': 'series1, series101'
        }
        Series.objects.create(**series_payload)
        url = reverse('series-list')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Bearer {self._access_token}',
                                   HTTP_X_DEVICE_ID=self._device_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listing_of_sermons(self):
        create_sermon()
        url = reverse('sermon-lists')
        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=f'Bearer {self._access_token}',
                                   HTTP_X_DEVICE_ID=self._device_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)

    def test_unauthenticated_user_cannot_add_like(self):
        create_sermon()

        url = reverse('sermon-lists')
        response = self.client.get(url, format='json', HTTP_X_DEVICE_ID=self._device_token)

        sermon_id = response.json()['results'][0]['@id']
        like_url = f'{sermon_id}add_like/'
        response = self.client.patch(like_url, format='json', HTTP_X_DEVICE_ID=self._device_token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_add_like(self):
        create_sermon()

        url = reverse('sermon-lists')
        response = self.client.get(url, format='json', HTTP_X_DEVICE_ID=self._device_token)

        sermon_id = response.json()['results'][0]['@id']
        like_url = f'{sermon_id}add_like/'
        response = self.client.patch(like_url, format='json', HTTP_X_DEVICE_ID=self._device_token,
                                     HTTP_AUTHORIZATION=f'Bearer {self._access_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authenticated_user_cannot_like_sermon_twice(self):
        create_sermon()

        url = reverse('sermon-lists')
        response = self.client.get(url, format='json', HTTP_X_DEVICE_ID=self._device_token)

        sermon_id = response.json()['results'][0]['@id']
        like_url = sermon_id + "add_like/"
        self.client.patch(like_url, format='json', HTTP_X_DEVICE_ID=self._device_token,
                          HTTP_AUTHORIZATION=f'Bearer {self._access_token}')
        response = self.client.patch(like_url, format='json', HTTP_X_DEVICE_ID=self._device_token,
                                     HTTP_AUTHORIZATION=f'Bearer {self._access_token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_liked_by_user_returns_error_if_already_liked(self):
        create_sermon()
        url = reverse('sermon-lists')
        response = self.client.get(url, format='json', HTTP_X_DEVICE_ID=self._device_token)

        sermon_id = response.json()['results'][0]['@id']
        like_url = sermon_id + "add_bookmark/"
        self.client.patch(like_url, format='json', HTTP_X_DEVICE_ID=self._device_token,
                          HTTP_AUTHORIZATION=f'Bearer {self._access_token}')
        response = self.client.get(sermon_id + "liked_by_user", format='json', HTTP_X_DEVICE_ID=self._device_token,
                                   HTTP_AUTHORIZATION=f'Bearer {self._access_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_liked_by_user_returns_404_if_sermon_not_bookmarked(self):
        create_sermon()
        url = reverse('sermon-lists')
        response = self.client.get(url, format='json', HTTP_X_DEVICE_ID=self._device_token)

        sermon_id = response.json()['results'][0]['@id']
        response = self.client.get(sermon_id + "liked_by_user", format='json', HTTP_X_DEVICE_ID=self._device_token,
                                   HTTP_AUTHORIZATION=f'Bearer {self._access_token}')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_all_bookmarked_sermons(self):
        create_sermon()
        url = reverse('sermon-lists')
        # add bookmarks
        response = self.client.get(url, format='json', HTTP_X_DEVICE_ID=self._device_token)
        sermon_id = response.json()['results'][0]['@id']
        like_url = sermon_id + "add_bookmark/"
        self.client.patch(like_url, format='json', HTTP_X_DEVICE_ID=self._device_token,
                          HTTP_AUTHORIZATION=f'Bearer {self._access_token}')
        # list bookmarks
        response = self.client.get(reverse('sermon-bookmarks'), format='json', HTTP_X_DEVICE_ID=self._device_token,
                                   HTTP_AUTHORIZATION=f'Bearer {self._access_token}')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1


class SeriesTestCase(TestSetupMixin, APITestCase):
    def test_user_can_bookmark_series(self):
        create_series()
        url = reverse('series-list')
        response = self.client.get(url, format='json', HTTP_X_DEVICE_ID=self._device_token)
        series_id = response.json()['results'][0]['@id']
        add_to_bookmark = f'{series_id}add_bookmark/'
        patch_response = self.client.patch(add_to_bookmark, format='json', HTTP_X_DEVICE_ID=self._device_token,
                                           HTTP_AUTHORIZATION=f'Bearer {self._access_token}')
        assert patch_response.status_code == status.HTTP_204_NO_CONTENT

    def test_user_cannot_bookmark_series_twice(self):
        create_series()
        url = reverse('series-list')
        response = self.client.get(url, format='json', HTTP_X_DEVICE_ID=self._device_token)
        series_id = response.json()['results'][0]['@id']
        add_to_bookmark = f'{series_id}add_bookmark/'
        self.client.patch(add_to_bookmark, format='json', HTTP_X_DEVICE_ID=self._device_token,
                          HTTP_AUTHORIZATION=f'Bearer {self._access_token}')
        patch_response = self.client.patch(add_to_bookmark, format='json', HTTP_X_DEVICE_ID=self._device_token,
                                           HTTP_AUTHORIZATION=f'Bearer {self._access_token}')
        assert patch_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_liked_by_user_returns_200_ok_when_already_liked(self):
        create_series()
        url = reverse('series-list')
        response = self.client.get(url, format='json', HTTP_X_DEVICE_ID=self._device_token)

        series_id = response.json()['results'][0]['@id']
        like_url = series_id + "add_bookmark/"
        self.client.patch(like_url, format='json', HTTP_X_DEVICE_ID=self._device_token,
                          HTTP_AUTHORIZATION=f'Bearer {self._access_token}')
        response = self.client.get(series_id + "liked_by_user/", format='json', HTTP_X_DEVICE_ID=self._device_token,
                                   HTTP_AUTHORIZATION=f'Bearer {self._access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_list_all_bookmarked_series(self):
        create_series()
        url = reverse('series-list')
        # add bookmarks
        response = self.client.get(url, format='json', HTTP_X_DEVICE_ID=self._device_token)
        series_id = response.json()['results'][0]['@id']
        like_url = series_id + "add_bookmark/"
        self.client.patch(like_url, format='json', HTTP_X_DEVICE_ID=self._device_token,
                          HTTP_AUTHORIZATION=f'Bearer {self._access_token}')
        # list bookmarks
        response = self.client.get(reverse('series-bookmarks'), format='json', HTTP_X_DEVICE_ID=self._device_token,
                                   HTTP_AUTHORIZATION=f'Bearer {self._access_token}')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
