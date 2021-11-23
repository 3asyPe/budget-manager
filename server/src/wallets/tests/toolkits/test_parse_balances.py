import pytest

from app.errors import ValidationError
from app.utils import AppErrorMessages
from wallets.services import WalletToolkit


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def balances(private_currency, public_currency):
    return [
        {"currency_name": private_currency.name},
        {"currency_name": public_currency.name}
    ]


def test_parse_balances(user, balances):
    new_balances = WalletToolkit.parse_balances(user, balances)
    for balance, new_balance in zip(balances, new_balances):
        assert new_balance["currency"].name == balance["currency_name"]


def test_parse_balances_without_required_field(user):
    balances = [{}]

    with pytest.raises(ValidationError) as exc:
        new_balances = WalletToolkit.parse_balances(user, balances)
    
    assert str(exc.value) == AppErrorMessages.REQUEST_FIELDS_ERROR.value