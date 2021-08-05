from django.urls import path

from currencies.api import apis


urlpatterns = [
     path('api/currency/create/', apis.create_currency_api)
]
