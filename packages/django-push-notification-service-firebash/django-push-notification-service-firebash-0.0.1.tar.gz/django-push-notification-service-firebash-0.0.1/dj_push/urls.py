from dj_push.models import DeviceToken
from django.urls import path
from dj_push.views import *

urlpatterns = [
    path('device/token/create', DeviceTokenCreateView.as_view()),
    path('device/token/get', DeviceTokenCreateView.as_view()),
    path('', MessageView.as_view())
]
