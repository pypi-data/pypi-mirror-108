django_firebash_push_service

Requirements

python >= 3.6
django >= 3
djangorestframework
requests

Installable App

This app can be installed and used in your django project by:

$ pip install django-firebash-push-service
Edit your settings.py file to include 'dj_push' in the INSTALLED_APPS listing.


INSTALLED_APPS = [
    ...

    'dj_push.apps.DjPushConfig',
]

also add SERVER_TOKEN in your setting.

you can get SERVER_TOKEN from firebash.

Edit your project urls.py file to import the URLs:
from dj_push.urls import urlpatterns

url_patterns = [
    ...
] + urlpatterns

Finally, add the models to your database:

$ ./manage.py migrate


The "project" Branch
The master branch contains the final code for the PyPI package. There is also a project branch which shows the "before" case -- the Django project before the app has been removed.

$ Guide

First save device token 

$ api_endpoint = domain + 'device/token/create', Use this endpoint for creating device token
$ payload = {
$    "token": device_token,
$    "device_os: "android"
$ }

$ api_endpoint = domain + 'device/token/get', Use this endpoint for get device token


after save token use this method for send notification
notice = NotificationSend(user=user_id, message=message, title=title)
response_msg = notice.send_device_notification()



Docs & Source
Article: https://pypi.org/user/bajpairitesh878/
Source: https://gitlab.com/bajpairitesh878/django_firebash_push_service
PyPI: https://pypi.org/user/bajpairitesh878/