from django.contrib import admin
from dj_push.models import *

# Register your models here.
class PushNotificationAdminView(admin.ModelAdmin):
    list_display = ('id', 'user', 'token', 'device_os', 'created_date')
    list_filter = ('user', 'device_os', 'created_date')
    search_fields = ('user', 'token')


admin.site.register(DeviceToken, PushNotificationAdminView)