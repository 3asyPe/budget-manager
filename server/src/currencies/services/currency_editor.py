from rest_framework.response import Response

from currencies.models import Currency
from app.errors import ValidationError
from currencies.utils import CurrencyErrorMessages


class CurrencyEditor:
    def __init__(self, name, new_name, new_code):
        self.name = name
        self.new_name = new_name
        self.new_code = new_code
        self.currency = self.get_currency()

    def __call__(self, raise_exception=True):
        if self.allowed_to_edit(raise_exception=raise_exception):
            return self.edit_currency()
        return self.currency

    def get_currency(self):
        return Currency.objects.get(name=self.name)

    def edit_currency(self):
        self.currency.name = self.new_name
        self.currency.code = self.new_code
        self.currency.save()
        return self.currency

    def allowed_to_edit(self, raise_exception=True):
        try:
            if len(self.new_code) != 3:
                raise ValidationError(CurrencyErrorMessages.WRONG_CURRENCY_CODE_ERROR.value)
            if not Currency.objects.filter(name=self.name).exists():
                raise ValidationError(CurrencyErrorMessages.CURRENCY_DOES_NOT_EXIST_ERROR.value)
            if Currency.objects.filter(name=self.new_name).exists():
                raise Response({'error': f'Currency with name - {self.new_name} already exists'}, 400)
            if 3 > len(self.name) > 25:
                raise Response({'error': 'Wrong name'})
        except (Currency.DoesNotExist, ValidationError) as exc:
            if raise_exception:
                raise exc
            return False
        return True

