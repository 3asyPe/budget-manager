from accounts.models import User
from currencies.services import CurrencyToolkit
from wallets.services import WalletCreator


class WalletToolkit:
    @classmethod
    def create_wallet(cls, user, name, start_balance, currency_name):
        currency = CurrencyToolkit.get_currency(user=user, currency_name=currency_name)
        return WalletCreator(
            user=user,
            name=name,
            start_balance=start_balance,
            currency=currency,
        )()
