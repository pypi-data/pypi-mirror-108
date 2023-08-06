import re
from dj_push.models import DeviceToken
from dj_push.serializers import DeviceTokenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status, authentication
import requests
from django.conf import settings
import json

# Create your views here.
class DeviceTokenCreateView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request):
        query = DeviceToken.objects.filter(user=request.user)
        if query:
            serializer = DeviceTokenSerializer(data=query, many=True)
            return Response(serializer.data)
        context = {'message': 'There is no device register with this user'}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        payload = {
            'user': request.user.pk,
            'token': request.data['token'],
            'device_os': request.data['device_os']
        }

        serializer = DeviceTokenSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request):
        notice = NotificationSend(user=request.data['user'], message=request.data['message'], title=request.data['title'])
        # print('send',notice.send_device_notification())
        response_msg = notice.send_device_notification()
        return Response({'message': response_msg})

class NotificationSend:
    """
    This class contain all the method related user phone notification.
    __init__ -- Need to pass user and message for notification.
    """

    def __init__(self, user=None, message="", title=""):
        self.title = title
        self.user = user
        self.message = message
        # self.send_device_notification()

    def get_device_token(self, *args, **kwargs):
        try:
            return DeviceToken.objects.filter(user=self.user).last().token

        except:
            return None
        

    def send_device_notification(self, *args, **kwargs):
        token = self.get_device_token()

        if token is None:
            return {'message': 'There is no device token register with this user', 'status': 400}
        
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'key=' + settings.SERVER_TOKEN,
            }
            body = {
                'notification': {'title': self.title, 'body': self.message},
                'to': token,
                'priority': 'high',
            }
            response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
            return response.json()

        except Exception as e:
            return e