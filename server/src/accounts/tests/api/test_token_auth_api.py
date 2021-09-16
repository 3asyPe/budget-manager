import pytest

from rest_framework.authtoken.models import Token

from accounts.utils import AccountErrorMessages


pytestmark = [pytest.mark.django_db]


def test_auth_with_existing_user(anon, user, user_token):
    response = anon.post(
        '/api/user/login/', {
            "username": "test@gmail.com",
            "password": "testpassword",
        },
        expected_status_code=200
    )

    assert response["token"] == user_token.key
    assert response["id"] == user.id
    assert response["email"] == user.email
    assert response["first_name"] == user.first_name
    assert response["second_name"] == user.second_name


def test_auth_with_user_without_token(anon, user):
    Token.objects.filter(user=user).delete()
    response = anon.post(
        '/api/user/login/', {
            "username": "test@gmail.com",
            "password": "testpassword"
        },
        expected_status_code=200
    )

    assert response["token"]
    assert response["id"] == user.id


@pytest.mark.parametrize("email, password", [
    ["non-existent-email@gmail.com", "randompassword"],
    ["test@gmail.com", "asdf"],
    ["email@gmail.com", "testpassword"],
])
def test_auth_with_wrong_credentials(anon, user, email, password):
    response = anon.post(
        '/api/user/login/', {
            "username": email,
            "password": password,
        }, 
        expected_status_code=400
    )

    assert response["error"] == AccountErrorMessages.CREDENTIALS_ERROR.value


def test_auth_with_inactive_user(anon, user):
    user.is_active = False
    user.save()
    
    response = anon.post(
        '/api/user/login/', {
            "username": "test@gmail.com",
            "password": "testpassword",
        },
        expected_status_code=400
    )

    assert response["error"] == AccountErrorMessages.DISABLED_ACCOUNT_ERROR.value

