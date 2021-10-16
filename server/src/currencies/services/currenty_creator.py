from accounts.models import Account
from app.errors import ObjectAlreadyExists, ValidationError
from currencies.models import Currency
from currencies.utils import CurrencyErrorMessages


class CurrencyCreator:
    def __init__(self, name:str, code:str, account:Account):
        self.name = name
        self.code = code
        self.account = account

    def __call__(self, raise_exception=True):
        if self.allowed_to_create(raise_exception):
            return self.create()
        else:
            return None

    def create(self):
        return Currency.objects.create(
            name=self.name,
            code=self.code,
            account=self.account,
        )

    def allowed_to_create(self, raise_exception=True):
        try:
            if Currency.objects.filter(name=self.name, public=False, account=self.account).exists():
                raise ObjectAlreadyExists
            if Currency.objects.filter(name=self.name, public=True):
                raise ObjectAlreadyExists
            if self.code is not None and len(self.code) != 3:
                raise ValidationError(CurrencyErrorMessages.WRONG_CURRENCY_CODE_ERROR.value)
            if len(self.name) > 25 or len(self.name) < 3:
                raise ValidationError(CurrencyErrorMessages.WRONG_CURRENCY_NAME_ERROR.value)
        except (ObjectAlreadyExists, ValidationError) as exc:
            if raise_exception:
                raise exc
            else:
                return False
        return True
