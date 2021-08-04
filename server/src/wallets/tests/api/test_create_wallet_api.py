import pytest

from app.utils import AppErrorMessages
from currencies.utils import CurrencyErrorMessages
from wallets.utils import WalletErrorMessages


pytestmark =[pytest.mark.django_db]


@pytest.fixture
def create_wallet(api, **kwargs):
    return lambda **kwargs: api.post(
        "/api/wallet/create/", {
            **kwargs,
        },
        expected_status_code=(kwargs.get("expected_status_code", 201))
    )


def test_wallet_creation_api(create_wallet, balances):
    wallet = create_wallet(
        name="Test wallet",
        balances=balances
    )

    assert wallet["id"]
    assert wallet["name"] == "Test wallet"
    assert wallet["is_hidden"] == False
    
    balances = wallet["balances"]
    for balance in balances:
        assert balance["currency"]["name"]
        assert "code" in balance["currency"]
        assert balance["amount"]
        assert "main" in balance


def test_wallet_creation_api_with_anonymous_user(anon, balances):
    anon.post(
        "/api/wallet/create/", {
            "name": "Test wallet",
            "balances": balances,
        },
        expected_status_code=401
    )


def test_wallet_creation_api_with_wrong_name(create_wallet, balances):
    response = create_wallet(
        name="",
        balances=balances,
        expected_status_code=400
    )

    assert response["error"] == WalletErrorMessages.WRONG_WALLET_NAME_ERROR.value


def test_already_existen_wallet_creation_api(create_wallet, wallet, balances):
    response = create_wallet(
        name=wallet.name,
        balances=balances,
        expected_status_code=400
    )

    assert response["error"] == AppErrorMessages.OBJECT_ALREADY_EXISTS_ERROR.value


def test_wallet_creation_api_with_non_existen_currency(create_wallet, balances):
    balances[0]["currency_name"] = "Some random name"
    response = create_wallet(
        name="Test wallet",
        balances=balances,
        expected_status_code=404
    )
    
    assert response["error"] == CurrencyErrorMessages.CURRENCY_DOES_NOT_EXIST_ERROR.value
