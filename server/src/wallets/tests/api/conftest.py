import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def balances(currency, public_currency):
    return [
        {
            "amount": 1.00,
            "currency_name": currency.name
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