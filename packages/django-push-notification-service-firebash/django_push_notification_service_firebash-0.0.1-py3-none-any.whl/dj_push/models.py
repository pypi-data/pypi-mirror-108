from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class DeviceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    token = models.CharField(max_length=1000, default='')
    device_os = models.CharField(max_length=100, default='')
    created_date = models.DateField(auto_now=True)
