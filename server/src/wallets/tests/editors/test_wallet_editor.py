import pytest

from wallets.services import WalletEditor


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
