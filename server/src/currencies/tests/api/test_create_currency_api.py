import pytest


pytestmark = [pytest.mark.django_db]


def test_creating_currency_api(api):
    response = api.post(
        '/api/currency/create/',
        {
            "name": "USD",
            "code": "USD",
        }
    )

    assert response["name"] == "USD"
    assert response["code"] == "USD"


def test_creating_already_existen_private_currency_api(api, private_currency):
    response = api.post(
        '/api/currency/create/',
        {
            "name": private_currency.name,
            "code": "USD",
        },
        expected_status_code=400
    )

    assert response["error"] == "CURRENCY_ALREADY_EXISTS_ERROR"


def test_creating_public_currency_api(api, public_currency):
    response = api.post(
        '/api/currency/create/',
        {
            "name": public_currency.name,
            "code": "USD",
        },
        expected_status_code=400
    )

    assert response["error"] == "CURRENCY_ALREADY_EXISTS_ERROR"


@pytest.mark.parametrize("code", ["U", "USDT"])
def test_creating_currency_api_with_wrong_code(api, code):
    response = api.post(
        '/api/currency/create/',
        {
            "name": "USD",
            "code": code,
        },
        expected_status_code=400
    )

    assert response["error"] == "WRONG_CURRENCY_CODE_ERROR"


@pytest.mark.parametrize("name", ["US", "SUPERMEGAULTRALOOOOOOOOOOOOONGCURRRENCYNAME"])
def test_creating_currency_api_with_wrong_name(api, name):
    response = api.post(
        '/api/currency/create/',
        {
            "name": name,
            "code": "USD",
        },
        expected_status_code=400
    )

    assert response["error"] == "WRONG_CURRENCY_NAME_ERROR"


def test_creating_currency_api_with_anonymous_user(anon):
    response = anon.post(
        '/api/currency/create/',
        {
            "name": "USD",
            "code": "USD",
        },
        expected_status_code=401
    )
