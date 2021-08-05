import pytest

from app.errors import ValidationError
from wallets.models import Wallet
from wallets.services import WalletEditor
from wallets.utils import WalletErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def balances(wallet, currency, public_currency):
    return [
        {
            "currency": currency,
            "amount": 19.00,
        },
        {
            "currency": public_currency,
            "amount": 13.00,
        }
    ]


def test_wallet_editing(wallet, balances, currency, public_currency):
    balance = wallet.balances.first()

    new_wallet = WalletEditor(
        id=wallet.id,
        user=wallet.user,
        name="New test name",
        balances=balances,
    )()

    assert new_wallet.id == wallet.id
    assert new_wallet.name == "New test name"
    
    first_balance = new_wallet.balances.first()
    assert first_balance.id == balance.id
    assert first_balance.currency == currency
    assert first_balance.amount == 19.00

    second_balance = new_wallet.balances.last()
    assert second_balance.currency == public_currency
    assert second_balance.amount == 13.00


def test_non_existen_wallet_editing(wallet, balances):
    with pytest.raises(Wallet.DoesNotExist):
        WalletEditor(
            id=wallet.id+123,
            user=wallet.user,
            name="New test name",
            balances=balances,
        )()


@pytest.mark.parametrize("name", [
    "", 
    "toooooooooooo looooooooooooong wallllllleeeeeeettttt naaaaaaaaaameeeeee"
])
def test_wallet_editing_with_wrong_name(wallet, balances, name):
    with pytest.raises(ValidationError) as exc:
        WalletEditor(
            id=wallet.id,
            user=wallet.user,
            name=name,
            balances=balances
        )()
    
    assert str(exc.value) == WalletErrorMessages.WRONG_WALLET_NAME_ERROR.value


def test_wallet_creation_with_raise_exception_false(wallet, balances):
    new_wallet = WalletEditor(
        id=wallet.id,
        user=wallet.user,
        name="",
        balances=balances,
    )(raise_exception=False)

    assert wallet == new_wallet
