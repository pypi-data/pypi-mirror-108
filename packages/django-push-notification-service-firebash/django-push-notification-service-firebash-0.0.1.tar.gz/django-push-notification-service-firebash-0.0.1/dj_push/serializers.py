from django.db.models import fields
from rest_framework import serializers
from dj_push.models import *

class DeviceTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceToken
        fields = "__all__"
