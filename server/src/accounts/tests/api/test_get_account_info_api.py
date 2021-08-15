import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def account(api, account):
    api.user.account = account
    api.user.owner = True
    api.user.save()
    return account


def test_getting_account_info_api(api, account):
    response = api.get('/api/account/get/info/', {})

    user = api.user
    r_user = response["users"][0]
    assert r_user["id"] == user.id
    assert r_user["first_name"] == user.first_name
    assert r_user["second_name"] == user.second_name
    assert "wallets" in r_user
    assert "totals" in r_user

    assert "totals" in response
