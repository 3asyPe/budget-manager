from typing import Optional, Union, List

from app.errors import ValidationError
from app.utils import AppErrorMessages
from accounts.models import User
from currencies.services import CurrencyToolkit
from wallets.models import Wallet
from wallets.services import WalletCreator, WalletEditor


class WalletToolkit:
    @classmethod
    def create_wallet(cls, user: User, name: str, balances: list) -> Wallet:
        balances = cls.parse_balances(user=user, balances=balances)
        return WalletCreator(
            user=user,
            name=name,
            balances=balances,
        )()

    @classmethod
    def edit_wallet(cls, wallet_id: Union[str, int], user, name, balances: list) -> Wallet:
        balances = cls.parse_balances(user=user, balances=balances)
        return WalletEditor(
            id=wallet_id,
            user=user,
            name=name,
            balances=balances
        )()

    @classmethod
    def delete_wallet(cls, wallet_id: Union[str, int]) -> bool:
        wallet = cls.get_wallet(wallet_id=wallet_id)
        wallet.delete()
        return True

    @classmethod
    def get_wallet(cls, wallet_id: Union[str, int], raise_exception=True) -> Optional[Wallet]:
        try:
            return Wallet.objects.get(id=wallet_id)
        except Wallet.DoesNotExist as exc:
            if raise_exception:
                raise exc
            return None

    @classmethod
    def get_wallets_by_user(cls, user: User, show_hidden=False) -> List[Wallet]:
        if show_hidden:
            return Wallet.objects.filter(user=user).all()
        else:
            return Wallet.objects.filter(user=user, is_hidden=False).all()

    @classmethod
    def parse_balances(cls, user, balances: list):
        for balance in balances:
            try:
                currency_name = balance["currency_name"]
            except KeyError:
                raise ValidationError(AppErrorMessages.REQUEST_FIELDS_ERROR.value)

            currency = CurrencyToolkit.get_currency(user=user, name=currency_name)
            balance["currency"] = currency
        
        return balances

    @classmethod
    def get_user_totals(cls, user) -> dict:
        totals = {}
        for wallet in user.wallets.all():
            for balance in wallet.balances.all():
                currency_name = balance.currency.name
                if currency_name in totals:
                    totals[currency_name] += balance.amount
                else:
                    totals[currency_name] = balance.amount
        return totals

    @classmethod
    def get_account_totals(cls, account) -> dict:
        totals = {}
        for user in account.users.all():
            user_totals = cls.get_user_totals(user)
            for currency_name in user_totals:
                if currency_name in totals:
                    totals[currency_name] += user_totals[currency_name]
                else:
                    totals[currency_name] = user_totals[currency_name]
        return totals
