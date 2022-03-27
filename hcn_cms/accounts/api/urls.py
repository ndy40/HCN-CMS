from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    DeviceDetailView,
    DeviceRegisterView,
    DevicesListView,
    RegisterUserView,
    UserDetailView,
    display_password_form
)


app_name = 'accounts'

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

    # Password reset route
    path(r'send_reset_password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path(r'update_password/<str:token>', display_password_form, name='display_password_form')
]
