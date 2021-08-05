import pytest

from currencies.utils import CurrencyErrorMessages
from wallets.utils import WalletErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def edit_wallet(api, **kwargs):
    return lambda **kwargs: api.put(
        f"/api/wallet/{kwargs['id']}/edit/", {
            **kwargs,
        },
        expected_status_code=(kwargs.get("expected_status_code", 200))
    )


@pytest.fixture
def balances(wallet, currency, public_currency):
    return [
        {
            "currency_name": currency.name,
            "amount": 19.00,
        },
        {
            "currency_name": public_currency.name,
            "amount": 13.00,
        }
    ]



def test_wallet_editing_api(edit_wallet, wallet, balances, currency, public_currency):
    balance = wallet.balances.first()

    new_wallet = edit_wallet(
        id=wallet.id,
        name="New test name",
        balances=balances,
    )

    assert new_wallet["id"] == wallet.id
    assert new_wallet["name"] == "New test name"

    first_balance = new_wallet["balances"][0]
    assert first_balance["id"] == balance.id
    assert first_balance["currency"]["name"] == currency.name
    assert float(first_balance["amount"]) == 19.00

    second_balance = new_wallet["balances"][1]
    assert second_balance["currency"]["name"] == public_currency.name
    assert float(second_balance["amount"]) == 13.00


def test_wallet_editing_api_with_anonymous_user(anon, wallet, balances):
    anon.put(
        f"/api/wallet/{wallet.id}/edit/", {
            "name": "Test wallet",
            "balances": balances,
        },
        expected_status_code=401
    )


def test_wallet_editing_api_with_wrong_name(edit_wallet, wallet, balances):
    response = edit_wallet(
        id=wallet.id,
        name='',
        balances=balances,
        expected_status_code=400
    )

    assert response["error"] == WalletErrorMessages.WRONG_WALLET_NAME_ERROR.value


def test_nonexisten_wallet_editing_api(edit_wallet, wallet, balances):
    response = edit_wallet(
        id=wallet.id+123,
        name="New test name",
        balances=balances,
        expected_status_code=404
    )

    assert response["error"] == WalletErrorMessages.WALLET_DOES_NOT_EXIST_ERROR.value


def test_wallet_editing_api_with_non_existen_currency(edit_wallet, wallet, balances):
    balances[0]["currency_name"] = "Some random name"
    response = edit_wallet(
        id=wallet.id,
        name="New test name",
        balances=balances,
        expected_status_code=404
    )

    assert response["error"] == CurrencyErrorMessages.CURRENCY_DOES_NOT_EXIST_ERROR.value
    