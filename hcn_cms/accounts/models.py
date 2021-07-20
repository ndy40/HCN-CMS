from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    class Meta:
        unique_together = ['email', 'is_staff']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_username()}"


class Device(models.Model):
    DEVICE_STATUS = [
        ('ACTIVE', 'Active'),
        ('DISABLED', 'Disabled')
    ]
    token = models.CharField(max_length=255, unique=True)
    phone_model = models.CharField(max_length=255)
    os_name = models.CharField(max_length=255)
    os_version = models.CharField(max_length=255)
    wifi = models.BooleanField(null=True)
    bluetooth = models.BooleanField(null=True)
    manufacturer = models.CharField(max_length=255)
    screen_width = models.CharField(max_length=255)
    screen_height = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=255, choices=DEVICE_STATUS)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='devices')

    @property
    def is_active(self):
        return 'ACTIVE' == self.status


class DeviceConsent(models.Model):
    push_notification = models.BooleanField(default=True)
    device = models.OneToOneField(Device, on_delete=models.CASCADE, primary_key=True, related_name='consent')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_member = models.BooleanField(null=True, default=False)
    year_joined = models.DateField(null=True, blank=True)
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    rest_token_expires = models.DateTimeField(null=True, blank=True)
