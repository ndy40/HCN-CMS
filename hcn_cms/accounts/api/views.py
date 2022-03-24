from django.db import transaction

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .permissions import HasDeviceHeader
from .serializers import DeviceSerializer, RegisterUserSerializer, UserSerializer
from .services import attach_device_to_user
from accounts.models import Device, User


class DeviceRegisterView(CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [AllowAny]


class DevicesListView(ListAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)


class DeviceDetailView(RetrieveUpdateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class RegisterUserView(CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny | HasDeviceHeader]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        if request.device:
            attach_device_to_user(user_id=serializer.data.get('id'), device=request.device)
            serializer = UserSerializer(instance=User.objects.get(pk=serializer.data.get('id')),
                                        context={'request': request})

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, HasDeviceHeader]
