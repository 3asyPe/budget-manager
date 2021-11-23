import pytest


pytestmark = [pytest.mark.django_db]


def test_getting_private_currency_api(api, private_currency):
    response = api.get(
        f"/api/currency/{private_currency.id}/get/",
    )