from accounts.models import Device
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView

from .serializers import DeviceSerializer


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
