import pytest

from wallets.models import Wallet
from wallets.utils import WalletErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def delete_wallet(api, **kwargs):
    return lambda **kwargs: api.delete(
        f"/api/wallet/{kwargs['id']}/delete/", {
            **kwargs
        },
        expected_status_code=kwargs.get("expected_status_code", 204),
        empty_content=kwargs.get("empty_content", False),
    )


def test_wallet_deleting_api(delete_wallet, wallet):
    delete_wallet(id=wallet.id, empty_content=True)

    assert not Wallet.objects.filter(id=wallet.id).exists()


def test_wallet_deleting_api_with_anonymous_user(anon, wallet):
    anon.delete(
        f"/api/wallet/{wallet.id}/delete/", 
        {},
        expected_status_code=401
    )


def test_non_existen_wallet_deleting_api(delete_wallet, wallet):
    response = delete_wallet(id=wallet.id+123, expected_status_code=404)

    assert response["error"] == WalletErrorMessages.WALLET_DOES_NOT_EXIST_ERROR.value