from django.urls import path

from .views import DevicesListView, DeviceDetailView, DeviceRegisterView


urlpatterns = [
    path('devices/register', DeviceRegisterView.as_view(), name="device-create"),
    path('devices/', DevicesListView.as_view(), name='device-list'),
    path('devices/<int:pk>', DeviceDetailView.as_view(), name="device-detail"),
]
