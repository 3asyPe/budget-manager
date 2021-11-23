import pytest

from currencies.utils import CurrencyErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def edit_currency(api):
    def edit(currency_id, **kwargs):
        return api.put(
            f"/api/currency/{currency_id}/edit/", {
                "new_name": kwargs.pop("new_name", "new name"),
                "new_code": kwargs.pop("new_code", "EUR")
            },
            empty_content=kwargs.pop('empty_content', False),
            expected_status_code=kwargs.pop("expected_status_code", 200)
        )
    return edit


def test_editing_currency_api(edit_currency, private_currency):
    response = edit_currency(private_currency.id)

    private_currency.refresh_from_db()

    assert response["name"] == private_currency.name == "new name"
    assert response["code"] == private_currency.code == "EUR"


def test_editing_public_currency_api(edit_currency, public_currency):
    response = edit_currency(
        public_currency.id,
        expected_status_code=404
    )

    
def test_editing_non_existen_currency_api(edit_currency, private_currency):
    response = edit_currency(
        private_currency.id + 123,
        expected_status_code=404
    )


@pytest.mark.parametrize("code", ("", "US", "USDT"))
def test_editing_currency_api_with_wrong_code(edit_currency, private_currency, code):
    response = edit_currency(
        private_currency.id,
        new_code=code,
        expected_status_code=400
    )

    assert response["error"] == CurrencyErrorMessages.WRONG_CURRENCY_CODE_ERROR.value


@pytest.mark.parametrize("name", ("", "long long name"))
def test_editing_currency_api_with_wrong_name(edit_currency, private_currency, name):
    response = edit_currency(
        private_currency.id,
        new_name=name,
        expected_status_code=400
    )

    assert response["error"] == CurrencyErrorMessages.WRONG_CURRENCY_NAME_ERROR.value


def test_editing_currency_api_already_existen_name(edit_currency, private_currency, public_currency):
    response = edit_currency(
        private_currency.id,
        new_name="USD",
        expected_status_code=400
    )

    assert response["error"] == CurrencyErrorMessages.CURRENCY_ALREADY_EXISTS_ERROR.value


def test_editing_currency_api_with_anonymous_user(anon, private_currency):
    response = anon.put(
        f"/api/currency/{private_currency.id}/edit/", {
            "new_name": "new name",
            "new_code": "EUR",
        },
        expected_status_code=401
    )