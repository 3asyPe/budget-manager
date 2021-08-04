from rest_framework.authtoken.models import Token

from accounts.models import User
from app.errors import ObjectAlreadyExists


class UserCreator:
    def __init__(self, username, first_name, second_name, password):
        self.username = str(username).lower()
        self.first_name = first_name
        self.second_name = second_name
        self.password = password

    def __call__(self, raise_exception=True):
        if self.allowed_to_create():
            user = self.create()
            user.first_name = self.first_name
            user.second_name = self.second_name
            user.save()
            return user
        else:
            return None

    def create(self):
        return User.objects.create_user(
            email=self.username,
            password=self.password,
        )

    #add validation
    def allowed_to_create(self, raise_exception=True):
        try:
            if User.objects.filter(email=self.username).exists():
                raise ObjectAlreadyExists
        except ObjectAlreadyExists as exc:
            if raise_exception:
                raise exc
            else:
                return False

        return True

    def after_creation(self, user):
        Token.objects.get_or_create(user=user)