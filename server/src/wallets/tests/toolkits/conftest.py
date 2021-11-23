import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def second_wallet(user, mixer, private_currency, public_currency):
    wallet = mixer.blend("wallets.Wallet", user=user)
    balance = mixer.blend("wallets.WalletBalance", amount=1.00, wallet=wallet, currency=private_currency, main=True)
    balance = mixer.blend("wallets.WalletBalance", amount=4.00, wallet=wallet, currency=public_currency, main=False)
    return wallet

@pytest.fixture
def third_wallet(user, mixer, public_currency):
    wallet = mixer.blend("wallets.Wallet", user=user)
    balance = mixer.blend("wallets.WalletBalance", amount=3.00, wallet=wallet, currency=public_currency, main=True)
    return wallet
