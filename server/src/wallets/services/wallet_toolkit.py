from app.errors import ValidationError
from app.utils import AppErrorMessages
from accounts.models import User
from currencies.services import CurrencyToolkit
from wallets.services import WalletCreator


class WalletToolkit:
    @classmethod
    def create_wallet(cls, user: User, name: str, balances: list):
        balances = cls.parse_balances(user=user, balances=balances)
        return WalletCreator(
            user=user,
            name=name,
            balances=balances,
        )()

    @classmethod
    def parse_balances(cls, user, balances: list):
        for balance in balances:
            try:
                currency_name = balance["currency_name"]
            except KeyError:
                raise ValidationError(AppErrorMessages.REQUEST_FIELDS_ERROR.value)

            currency = CurrencyToolkit.get_currency(user=user, currency_name=currency_name)
            balance["currency"] = currency
        
        return balances