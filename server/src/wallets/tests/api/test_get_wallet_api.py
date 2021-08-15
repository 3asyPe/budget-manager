import pytest

from wallets.utils import WalletErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def get_wallet(api, **kwargs):
    return lambda **kwargs: api.get(
        f"/api/wallet/{kwargs['id']}/get/",
        expected_status_code=kwargs.get("expected_status_code", 200)
    )


def test_wallet_getting_api(get_wallet, wallet):
    r_wallet = get_wallet(id=wallet.id)

    assert r_wallet["id"] == wallet.id
    assert r_wallet["name"] == wallet.name
    assert r_wallet["is_hidden"] == wallet.is_hidden
    
    balance = wallet.balances.first()
    r_balance = r_wallet["balances"][0]
    assert r_balance["id"] == balance.id
    assert float(r_balance["amount"]) == float(balance.amount)
    assert r_balance["main"] == balance.main

    currency = balance.currency
    r_currency = r_balance["currency"]
    assert r_currency["id"] == currency.id
    assert r_currency["name"] == currency.name
    assert r_currency["code"] == currency.code


def test_wallet_getting_api_with_anonymous_user(anon, wallet):
    anon.get(
        f"/api/wallet/{wallet.id}/get/",
        expected_status_code=401
    )


def test_non_existen_wallet_getting_api(get_wallet, wallet):
    response = get_wallet(id=wallet.id+123, expected_status_code=404)

    assert response["error"] == WalletErrorMessages.WALLET_DOES_NOT_EXIST_ERROR.value
