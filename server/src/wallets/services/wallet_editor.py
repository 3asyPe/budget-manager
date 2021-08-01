from typing import Union, Optional

from app.errors import ValidationError
from accounts.models import User
from wallets.models import Wallet, WalletBalance


class WalletEditor:
    def __init__(self, id: Union[str, int], user: User, name: str, balances: list):
        self.id = id
        self.user = user
        self.name = name
        self.balances = balances
        self.wallet = self.get_wallet()

    def __call__(self, raise_exception=True) -> Optional[Wallet]:
        if self.allowed_to_edit(raise_exception=raise_exception):
            wallet = self.edit_wallet()
            for balance in self.balances:
                balance = self.edit_balance(balance)
            return wallet
        return None

    def get_wallet(self) -> Wallet:
        return Wallet.objects.get(id=self.id)

    def edit_wallet(self) -> Wallet:
        self.wallet.name = self.name
        self.wallet.save()
        return self.wallet

    def edit_balance(self, balance) -> WalletBalance:
        qs = WalletBalance.objects.filter(wallet=self.wallet, currency=balance["currency"])
        if not qs.exists():
            return WalletBalance.objects.create(
                wallet=self.wallet,
                currency=balance["currency"],
                amount=balance["amount"],
            )
        
        balance_obj = qs.first()
        balance_obj.amount = balance["amount"]
        balance_obj.save()
        return balance_obj

    def allowed_to_edit(self, raise_exception) -> bool:
        try:
            if not 0 < len(self.name) < 41:
                    raise ValidationError(WalletErrorMessages.TOO_LONG_WALLET_NAME_ERROR.value)

            if self.wallet is None:
                raise Wallet.DoesNotExist()
        except (Wallet.DoesNotExist, ValidationError) as exc:
            if raise_exception:
                raise exc
            return False
        return True
