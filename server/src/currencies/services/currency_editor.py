from currencies.models import Currency
from app.errors import ValidationError, ObjectAlreadyExists
from currencies.utils import CurrencyErrorMessages


class CurrencyEditor:
    def __init__(self, id, new_name, new_code):
        self.id = id
        self.new_name = new_name
        self.new_code = new_code
        self.currency = self.get_currency()

    def __call__(self, raise_exception=True):
        if self.allowed_to_edit(raise_exception=raise_exception):
            return self.edit_currency()
        return self.currency

    def get_currency(self):
        return Currency.objects.get(id=self.id)

    def edit_currency(self):
        self.currency.name = self.new_name
        self.currency.code = self.new_code
        self.currency.save()
        return self.currency

    def allowed_to_edit(self, raise_exception=True):
        try:
            if len(self.new_code) != 3:
                raise ValidationError(CurrencyErrorMessages.WRONG_CURRENCY_CODE_ERROR.value)                
            if not Currency.objects.filter(id=self.id).exists():
                raise Currency.DoesNotExist()
            if Currency.objects.filter(name=self.new_name, public=True).exists():
               raise ObjectAlreadyExists()
            if len(self.new_name) > 25 or len(self.new_name) < 3:
                raise ValidationError(CurrencyErrorMessages.WRONG_CURRENCY_NAME_ERROR.value)
            if not Currency.objects.filter(id=self.id, public=False, account=self.currency.account).exists():
                raise ObjectAlreadyExists()
        except (Currency.DoesNotExist, ValidationError, ObjectAlreadyExists) as exc:
            if raise_exception:
                raise exc
            return False
        return True
