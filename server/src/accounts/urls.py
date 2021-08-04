from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from accounts import apis


urlpatterns = [
    path('api/user/create/', apis.create_user_api),
    path('api/user/login/', apis.authenticate_user_api),
]