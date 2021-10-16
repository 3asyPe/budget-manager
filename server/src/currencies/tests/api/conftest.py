import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def private_currency(api, currency):
    currency.account = api.user.account
    currency.save()
    return currency
