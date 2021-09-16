import pytest

from rest_framework.authtoken.models import Token

from accounts.services import UserCreator


pytestmark = [pytest.mark.django_db]


def test_auto_token_creation():
    user = UserCreator(
        username="newemail@gmail.com",
        first_name="Eric",
        second_name="Cartman",
        password="newpassword"
    )()

    assert Token.objects.get(user=user)