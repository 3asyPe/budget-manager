from rest_framework import serializers
from rest_framework.authtoken.models import Token

from accounts.models import User, Account
from wallets.api.serializers import WalletSerializer
from wallets.services import WalletToolkit


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'second_name',
            'token',
            'id',
        ]

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class UserInfoSerializer(serializers.ModelSerializer):
    wallets = WalletSerializer(many=True)
    totals = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'second_name',
            'wallets',
            'totals',
        ]

    def get_totals(self, obj):
        return WalletToolkit.get_user_totals(user=obj)


class AccountSerializer(serializers.ModelSerializer):
    users = UserInfoSerializer(many=True)
    totals = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            "users",
            "totals",
        ]

    def get_totals(self, obj):
        return WalletToolkit.get_account_totals(obj)
