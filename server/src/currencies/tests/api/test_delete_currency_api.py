import pytest

from currencies.models import Currency


pytestmark = [pytest.mark.django_db]


def test_deleting_currency_api(api, private_currency):
    response = api.delete(
        f"/api/currency/{private_currency.id}/delete/",
        empty_content=True
    )

    with pytest.raises(Currency.DoesNotExist):
        currency = Currency.objects.get(id=private_currency.id)


# def test_deleting_not_owned_private_currency_api(api, user, private_currency):

#     response = api.delete(
#         f"/api/currency/{}"
#     )


def test_deleting_non_existen_currency_api(api, private_currency):
    response = api.delete(
        f"/api/currency/{private_currency.id + 123}/delete/",
        expected_status_code=404
    )


def test_deleting_public_currency_api(api, public_currency):
    response = api.delete(
        f"/api/currency/{public_currency.id}/delete/",
        expected_status_code=404
    )


def test_deleting_currency_api_with_anonymous_user(anon, private_currency):
    response = anon.delete(
        f"/api/currency/{private_currency.id}/delete/",
        expected_status_code=401,
    )