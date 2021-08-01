from rest_framework import serializers

from currencies.api.serializers import CurrencySerializer
from wallets.models import Wallet, WalletBalance


class WalletBalanceSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = WalletBalance
        fields = [
            'currency',
            'amount',
            'main',
        ]


class WalletSerializer(serializers.ModelSerializer):
    balances = WalletBalanceSerializer(many=True)

    class Meta:
        model = Wallet
        fields = [
            'id',
            'name',
            'is_hidden',
            'balances',
        ]
