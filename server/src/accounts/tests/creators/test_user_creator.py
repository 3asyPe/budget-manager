import pytest

from accounts.services import UserCreator
from app.errors import ObjectAlreadyExists


pytestmark = [pytest.mark.django_db]


def test_user_creation():
    user = UserCreator(
        username="newemail@gmail.com",
        first_name="Eric",
        second_name="Cartman",
        password="newpassword"
    )()

    assert user.email == "newemail@gmail.com"
    assert user.first_name == "Eric"
    assert user.second_name == "Cartman"
    assert user.is_active == True

    assert user.account is not None
    assert user.owner == True


def test_already_existen_user_creation(user):
    with pytest.raises(ObjectAlreadyExists) as exc:
        new_user = UserCreator(
            username=user.email,
            first_name="Eric",
            second_name="Cartman",
            password="newpassword"
        )()


def test_user_creator_case_sensetivity(user):
    with pytest.raises(ObjectAlreadyExists) as exc:
        new_user = UserCreator(
            username="TeST@gmAiL.cOM",
            first_name="Eric",
            second_name="Cartman",
            password="newpassword"
        )()


def test_user_creation_raise_exception(user):
    new_user = UserCreator(
        username=user.email,
        first_name="Eric",
        second_name="Cartman",
        password="newpassword"
    )(raise_exception=False)

    assert new_user is None
