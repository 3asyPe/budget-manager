from rest_framework.authtoken.models import Token
from accounts import services
import accounts
from accounts.models import User
from app.errors import ValidationError
from accounts.utils import AccountErrorMessages

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


user = get_user_model()

class UserToolKit:
    @classmethod
    def creater_user(cls, username, first_name, second_name, password):
        from accounts.services import UserCreator
        user = UserCreator(
            username=username,
            first_name=first_name,
            second_name=second_name,
            password=password,
        )()
        return user


    @classmethod
    def authenticate_user(cls, email, password):
        user = authenticate(username=email, password=password)

        if not user:
            qs = User.objects.filter(username=email)
            if qs.exists() and not qs.first().is_active:
                raise ValidationError(AccountErrorMessages.DISABLED_ACCOUNT_ERROR.value)
            raise ValidationError(AccountErrorMessages.CREDENTIALS_ERROR.value)

        return user, Token.objects.get_or_create(user=user)[0]

