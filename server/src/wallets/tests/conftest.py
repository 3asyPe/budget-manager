import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def wallet(mixer, user, currency):
    wallet = mixer.blend("wallets.Wallet", user=user)
    balance = mixer.blend("wallets.WalletBalance", wallet=wallet, currency=currency, main=True)
    return wallet
