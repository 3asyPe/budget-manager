import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def second_balance(wallet, public_currency, mixer):
    return mixer.blend(
        "wallets.WalletBalance", 
        wallet=wallet, 
        currency=public_currency,
    )


def test_balance_is_main(wallet):
    balance = wallet.balances.first()

    assert wallet.main_balance == balance


def test_set_balance_as_main(wallet, second_balance):
    second_balance.set_as_main()

    assert wallet.main_balance == second_balance
