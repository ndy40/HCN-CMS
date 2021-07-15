from django.urls import path

from .views import DevicesListView, DeviceDetailView, DeviceRegisterView, RegisterUserView, UserDetailView


urlpatterns = [
    path('devices/register', DeviceRegisterView.as_view(), name="device-create"),
    path('devices/', DevicesListView.as_view(), name='device-list'),
    path('devices/<int:pk>', DeviceDetailView.as_view(), name="device-detail"),

    # User related paths
    path('users/register', RegisterUserView.as_view(), name='user-register'),
    path('users/<int:pk>', UserDetailView.as_view(), name='user-detail')

]
