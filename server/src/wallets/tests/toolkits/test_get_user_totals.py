import pytest

from wallets.services import WalletToolkit


pytestmark = [pytest.mark.django_db]


def test_getting_user_totals(
    user, 
    wallet, 
    second_wallet, 
    third_wallet, 
    private_currency,
    public_currency,
):
    totals = WalletToolkit.get_user_totals(user)

    first_sum = wallet.balances.first().amount + second_wallet.balances.first().amount
    assert float(totals[private_currency.name]) == float(first_sum)

    second_sum = second_wallet.balances.last().amount + third_wallet.balances.first().amount
    assert float(totals[public_currency.name]) == float(second_sum)
