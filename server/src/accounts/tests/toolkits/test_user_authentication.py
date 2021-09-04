import pytest

from accounts.services import UserToolKit


pytestmark = [pytest.mark.django_db]


def test_user_authentication(user, user_token):
    auth_user, token = UserToolKit.authenticate_user(
        email=user.email,
        password="testpassword"
    )

    assert auth_user == user
    assert token == user_token
    assert auth_user.is_authenticated