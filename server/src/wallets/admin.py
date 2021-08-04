from django.contrib import admin

from wallets.models import Wallet, WalletBalance


admin.site.register(Wallet)
admin.site.register(WalletBalance)
