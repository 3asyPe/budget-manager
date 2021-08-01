import pytest

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer as _mixer

from app.test.api_client import DRFClient


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def api():
    return DRFClient()


@pytest.fixture
def anon():
    return DRFClient(anon=True)


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def user(mixer):
    return mixer.blend("accounts.User", email="testemail@gmail.com")


@pytest.fixture
def another_user(mixer):
    return mixer.blend("accounts.User", email="testemail2@gmail.com")


@pytest.fixture
def anonymous_user(mixer):
    return AnonymousUser()
