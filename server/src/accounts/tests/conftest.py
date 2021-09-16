import pytest

from rest_framework.authtoken.models import Token


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def user(mixer):
    user = mixer.blend("accounts.User", email="test@gmail.com")
    user.set_password("testpassword")
    user.save()
    return user


@pytest.fixture
def user_token(user):
    return Token.objects.get_or_create(user=user)[0]