from django.urls import path

from wallets.api import apis


urlpatterns = [
    path("api/wallet/create/", apis.create_wallet_api),
    path("api/wallet/all/get/", apis.get_user_wallets_api),
    path("api/wallet/<int:id>/edit/", apis.edit_wallet_api),
    path("api/wallet/<int:id>/get/", apis.get_wallet_api),
    path("api/wallet/<int:id>/delete/", apis.delete_wallet_api),
]
