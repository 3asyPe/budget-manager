import pytest

from rest_framework.authtoken.models import Token

from accounts.models import Account, User
from accounts.utils import AccountErrorMessages


pytestmark = [pytest.mark.django_db]


def test_user_creation_api(anon):
    response = anon.post(
        '/api/user/create/', {
            "username": "newemail@gmail.com",
            "first_name": "Eric",
            "second_name": "Cartman",
            "password": "newpassword",
        }
    )

    new_user = User.objects.get(email="newemail@gmail.com")
    new_token = Token.objects.get(user=new_user)

    assert response["id"] == new_user.id
    assert response["email"] == new_user.email == "newemail@gmail.com"
    assert response["first_name"] == new_user.first_name == "Eric"
    assert response["second_name"] == new_user.second_name == "Cartman"
    assert response["token"] == new_token.key


def test_account_auto_creation_with_user_creation_api(anon):
    response = anon.post(
        '/api/user/create/', {
            "username": "newemail@gmail.com",
            "first_name": "Eric",
            "second_name": "Cartman",
            "password": "newpassword",
        }
    )

    new_user = User.objects.get(email="newemail@gmail.com")
    
    assert new_user.account is not None


def test_already_existen_user_creation_api(anon, user):
    response = anon.post(
        '/api/user/create/', {
            "username": user.email,
            "first_name": "Eric",
            "second_name": "Cartman",
            "password": "newpassword",
        },
        expected_status_code=400
    )

    assert response["error"] == AccountErrorMessages.NON_UNIQUE_EMAIL_ERROR.value
