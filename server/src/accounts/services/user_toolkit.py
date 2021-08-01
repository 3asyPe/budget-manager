from accounts import services
from accounts.models import User
from django.contrib.auth import get_user_model

user = get_user_model()

class UserToolKit:
    @classmethod
    def creater_user(cls, username, first_name, second_name, password):
        from accounts.services import UserCreator
        user = UserCreator(
            username=username,
            first_name=first_name,
            second_name=second_name,
            password=password
        )()
        return user