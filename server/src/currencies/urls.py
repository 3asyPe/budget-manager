from django.urls import path

from currencies.api import apis


urlpatterns = [
     path('api/currency/create/', apis.create_currency_api),
     path('api/currency/<int:id>/delete/', apis.delete_currency_api),
     path('api/currency/<int:id>/get/', apis.get_currency_api),
     path('api/currency/<int:id>edit/', apis.edit_currency_api),
     path('api/currency/get/account', apis.get_currencies_by_account_api)
]
