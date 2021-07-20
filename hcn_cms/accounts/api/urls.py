from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import DeviceDetailView, DeviceRegisterView, DevicesListView, RegisterUserView, UserDetailView


urlpatterns = [
    path('devices/register', DeviceRegisterView.as_view(), name="device-create"),
    path('devices/', DevicesListView.as_view(), name='device-list'),
    path('devices/<int:pk>/', DeviceDetailView.as_view(), name="device-detail"),

    # User related paths
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/register', RegisterUserView.as_view(), name='user-register'),

    # Simple JWT authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
