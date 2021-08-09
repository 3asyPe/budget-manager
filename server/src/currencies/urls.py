from django.urls import path

from currencies.api import apis


urlpatterns = [
     path('api/currency/create/', apis.create_currency_api),
     path('api/currency/delete/', apis.delete_currency_api),
     path('api/currency/get/', apis.get_currency_api),
     path('api/currency/put/', apis.edit_currency_api)
]
