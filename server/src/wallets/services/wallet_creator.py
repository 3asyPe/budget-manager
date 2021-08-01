from typing import Union, Optional

from app.errors import ValidationError, ObjectAlreadyExists
from accounts.models import User
from currencies.models import Currency
from wallets.models import Wallet, WalletBalance
from wallets.utils import WalletErrorMessages


class WalletCreator:
    def __init__(
        self, 
        user: User, 
        name: str, 
        balances: list,
    ):
        self.user = user
        self.name = name
        self.balances = balances

    def __call__(self,  raise_exception=True) -> Optional[Wallet]:
        if self.allowed_to_create(raise_exception=raise_exception):
            wallet = self.create_wallet()
            for i, balance in enumerate(self.balances):
                if i == 0:
                    balance = self.create_balance(wallet, balance, main=True)
                else:
                    balance = self.create_balance(wallet, balance, main=False)
            return wallet
        return None

    def create_wallet(self) -> Wallet:
        return Wallet.objects.create(
            user=self.user,
            name=self.name,
        )

    def create_balance(self, wallet, balance, main=False) -> WalletBalance:
        return WalletBalance.objects.create(
            wallet=wallet,
            currency=balance["currency"],
            amount=balance["amount"],
            main=main,
        )

    def allowed_to_create(self, raise_exception):
        try:
            qs = Wallet.objects.filter(user=self.user, name=self.name)
            if qs.exists():
                raise ObjectAlreadyExists()
            
            if not 0 < len(self.name) < 41:
                raise ValidationError(WalletErrorMessages.TOO_LONG_WALLET_NAME_ERROR.value)
        except (ObjectAlreadyExists, ValidationError) as exc:
            if raise_exception:
                raise exc
            return False
        return True
