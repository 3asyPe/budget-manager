import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def private_currency(api, private_currency):
    private_currency.account = api.user.account
    private_currency.save()
    return private_currency
