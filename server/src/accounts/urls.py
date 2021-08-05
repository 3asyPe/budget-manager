from django.urls import path

from accounts import apis


urlpatterns = [
    path('api/user/create/', apis.create_user_api),
    path('api/user/login/', apis.authenticate_user_api),
    ]