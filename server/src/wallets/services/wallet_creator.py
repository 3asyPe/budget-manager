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
        start_balance: Union[float, str], 
        currency: Currency,
    ):
        self.user = user
        self.name = name
        self.start_balance = start_balance
        self.currency = currency

    def __call__(self, raise_exception=True) -> Optional[Wallet]:
        if self.allowed_to_create(raise_exception=raise_exception):
            wallet = self.create_wallet()
            balance = self.create_balance(wallet)
            return wallet
        return None

    def create_wallet(self) -> Wallet:
        return Wallet.objects.create(
            user=self.user,
            name=self.name,
        )

    def create_balance(self, wallet) -> WalletBalance:
        return WalletBalance.objects.create(
            wallet=wallet,
            currency=self.currency,
            amount=self.start_balance,
            main=True,
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
