import pytest

from wallets.services import WalletToolkit


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def account(account, user, another_user):
    user.account = account
    user.owner = True
    user.save()

    another_user.account = account
    another_user.save()
    return account


@pytest.fixture
def fourth_wallet(mixer, another_user, currency, public_currency):
    wallet = mixer.blend("wallets.Wallet", user=another_user)
    balance = mixer.blend("wallets.WalletBalance", amount=2.00, wallet=wallet, currency=currency, main=True)
    balance = mixer.blend("wallets.WalletBalance", amount=2.00, wallet=wallet, currency=public_currency, main=False)
    return wallet


def test_getting_account_totals(
    account,
    wallet,
    second_wallet,
    third_wallet,
    fourth_wallet,
    currency,
    public_currency
):
    totals = WalletToolkit.get_account_totals(account)

    first_sum = wallet.balances.first().amount + second_wallet.balances.first().amount + fourth_wallet.balances.first().amount
    assert float(totals[currency.name]) == float(first_sum)

    second_sum = second_wallet.balances.last().amount + third_wallet.balances.first().amount + fourth_wallet.balances.last().amount
    assert float(totals[public_currency.name]) == float(second_sum)