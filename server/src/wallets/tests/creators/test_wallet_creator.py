import pytest

from app.errors import ValidationError, ObjectAlreadyExists
from wallets.models import Wallet
from wallets.services import WalletCreator
from wallets.utils import WalletErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def balances(private_currency, public_currency):
    return [
        {
            "currency": private_currency,
            "amount": 1.00
        },
        {
            "currency": public_currency,
            "amount": 1.00
        }
    ]


def test_wallet_creation(user, balances):
    wallet = WalletCreator(
        user=user,
        name="Test wallet",
        balances=balances,
    )()

    assert wallet.user == user
    assert wallet.name == "Test wallet"
    assert wallet.is_hidden == False

    balance = wallet.balances.first()
    assert float(balance.amount) == 1.00
    assert balance.currency == balances[0]["currency"]
    assert balance.main == True


@pytest.mark.parametrize("start_balance", [0.00, -123.2, 1231023, "1.00"])
def test_wallet_creation_with_any_start_balance(start_balance, user, private_currency):
    balances = [{
        "currency": private_currency,
        "amount": start_balance,
    }]
    wallet = WalletCreator(
        user=user,
        name="Test wallet",
        balances=balances,
    )()

    balance = wallet.balances.first()
    assert float(balance.amount) == float(start_balance)


@pytest.mark.parametrize("name", [
    "", 
    "toooooooooooo looooooooooooong wallllllleeeeeeettttt naaaaaaaaaameeeeee"
])
def test_wallet_creation_with_wrong_name(name, user, balances):
    with pytest.raises(ValidationError) as exc:
        wallet = WalletCreator(
            user=user,
            name=name,
            balances=balances,
        )()
    
    assert str(exc.value) == WalletErrorMessages.WRONG_WALLET_NAME_ERROR.value


def test_wallet_creation_with_already_used_name(wallet, user, balances):
    with pytest.raises(ObjectAlreadyExists):
        wallet = WalletCreator(
            user=user,
            name=wallet.name,
            balances=balances,
        )()


def test_wallet_creation_with_raise_exception_false(wallet, user, balances):
    wallet = WalletCreator(
        user=user,
        name=wallet.name,
        balances=balances,
    )(raise_exception=False)

    assert wallet is None
