import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def get_wallets(api, **kwargs):
    return lambda **kwargs: api.get(
        "/api/wallet/all/get/",{
            **kwargs
        },
        expected_status_code=kwargs.get("expected_status_code", 200)
    )


@pytest.fixture
def another_wallet(api, mixer, public_currency):
    wallet = mixer.blend("wallets.Wallet", user=api.user)
    balance = mixer.blend("wallets.WalletBalance", wallet=wallet, currency=public_currency)
    return wallet


def test_user_wallets_getting_api(get_wallets, wallet, another_wallet):
    wallets = get_wallets(
        show_hidden=True
    )

    for wallet, r_wallet in zip((wallet, another_wallet), wallets):
        assert r_wallet["id"] == wallet.id
        assert r_wallet["name"] == wallet.name
        assert r_wallet["is_hidden"] == wallet.is_hidden
        
        balance = wallet.balances.first()
        r_balance = r_wallet["balances"][0]
        assert r_balance["id"] == balance.id
        assert float(r_balance["amount"]) == balance.amount
        assert r_balance["main"] == balance.main

        currency = balance.currency
        r_currency = r_balance["currency"]
        assert r_currency["id"] == currency.id
        assert r_currency["name"] == currency.name
        assert r_currency["code"] == currency.code


def test_user_wallets_getting_api_show_hidden_false(get_wallets, wallet, another_wallet):
    another_wallet.is_hidden = True
    another_wallet.save()

    wallets = get_wallets(
        show_hidden=False
    )

    assert len(wallets) == 1


def test_user_wallets_getting_api_with_anonymous_user(anon, wallet):
    wallets = anon.get(
        "/api/wallet/all/get/",
        expected_status_code=401
    )
