from accounts.models import Device, User
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from .serializers import DeviceSerializer, RegisterUserSerializer, UserSerializer
from .services import attach_device_to_user


class DeviceRegisterView(CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DevicesListView(ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    # def get_queryset(self):
    #  TODO: when we add user support, we should filter devices.user == request.user.id to narrow search down.
    #     devices = Device.objects.filter()


class DeviceDetailView(RetrieveUpdateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class RegisterUserView(CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        if request.device:
            attach_device_to_user(user_id=serializer.data.get('id'), device=request.device)
            serializer = UserSerializer(instance=User.objects.get(pk=serializer.data.get('id')),
                                        context={'request': request})
            # serializer.is_valid(raise_exception=True)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all
    serializer_class = UserSerializer
