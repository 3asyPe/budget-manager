import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def balances(private_currency, public_currency):
    return [
        {
            "amount": 1.00,
            "currency_name": private_currency.name
        },
        {
            "amount": 1.00,
            "currency_name": public_currency.name
        }
    ]


@pytest.fixture
def wallet(api, wallet):
    wallet.user = api.user
    wallet.save()
    return wallet


@pytest.fixture
def private_currency(api, private_currency):
    private_currency.account = api.user.account
    private_currency.save()
    return private_currency