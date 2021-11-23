import pytest

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer as _mixer

from app.test.api_client import DRFClient


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def api():
    return DRFClient()


@pytest.fixture
def anon():
    return DRFClient(anon=True)


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def account(mixer):
    return mixer.blend("accounts.Account")
    

@pytest.fixture
def user(mixer, account):
    return mixer.blend("accounts.User", email="testemail@gmail.com", account=account)


@pytest.fixture
def another_user(mixer):
    return mixer.blend("accounts.User", email="testemail2@gmail.com")


@pytest.fixture
def anonymous_user(mixer):
    return AnonymousUser()


@pytest.fixture
def private_currency(mixer, user):
    return mixer.blend("currencies.Currency", public=False, account=user.account)


@pytest.fixture
def public_currency(mixer):
    return mixer.blend("currencies.Currency", name="USD", code="USD", public=True)


@pytest.fixture
def wallet(mixer, user, private_currency):
    wallet = mixer.blend("wallets.Wallet", user=user)
    balance = mixer.blend(
        "wallets.WalletBalance", 
        amount=3.23, 
        wallet=wallet, 
        currency=private_currency, 
        main=True
    )
    return wallet
