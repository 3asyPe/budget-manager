import pytest

from app.errors import ValidationError, ObjectAlreadyExists
from wallets.models import Wallet
from wallets.services import WalletCreator
from wallets.utils import WalletErrorMessages


pytestmark = [pytest.mark.django_db]


def test_wallet_creation(user, currency):
    wallet = WalletCreator(
        user=user,
        name="Test wallet",
        start_balance=1.00,
        currency=currency,
    )()

    assert wallet.user == user
    assert wallet.name == "Test wallet"
    assert wallet.is_hidden == False

    balance = wallet.balances.first()
    assert float(balance.amount) == 1.00
    assert balance.currency == currency
    assert balance.main == True


@pytest.mark.parametrize("start_balance", [0.00, -123.2, 1231023, "1.00"])
def test_wallet_creation_with_any_start_balance(start_balance, user, currency):
    wallet = WalletCreator(
        user=user,
        name="Test wallet",
        start_balance=start_balance,
        currency=currency
    )()

    balance = wallet.balances.first()
    assert float(balance.amount) == float(start_balance)


@pytest.mark.parametrize("name", [
    "", 
    "toooooooooooo looooooooooooong wallllllleeeeeeettttt naaaaaaaaaameeeeee"
])
def test_wallet_creation_with_wrong_name(name, user, currency):
    with pytest.raises(ValidationError) as exc:
        wallet = WalletCreator(
            user=user,
            name=name,
            start_balance=1.00,
            currency=currency,
        )()
    
    assert str(exc.value) == WalletErrorMessages.TOO_LONG_WALLET_NAME_ERROR.value


def test_wallet_creation_with_already_used_name(wallet, user, public_currency):
    with pytest.raises(ObjectAlreadyExists):
        wallet = WalletCreator(
            user=user,
            name=wallet.name,
            start_balance=1.00,
            currency=public_currency,
        )()


def test_wallet_creation_with_raise_exception_false(wallet, user, public_currency):
    wallet = WalletCreator(
        user=user,
        name=wallet.name,
        start_balance=1.00,
        currency=public_currency,
    )(raise_exception=False)

    assert wallet is None
