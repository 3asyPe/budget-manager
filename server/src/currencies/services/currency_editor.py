from rest_framework.response import Response

from currencies.models import Currency
from app.errors import ValidationError
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
                return Response({"error" : CurrencyErrorMessages.WRONG_CURRENCY_CODE_ERROR.value}, status=400)
            if not Currency.objects.filter(id=self.id).exists():
                return Response({"error" : CurrencyErrorMessages.CURRENCY_DOES_NOT_EXIST_ERROR.value}, status=400)
            if Currency.objects.filter(name=self.new_name, public=True).exists():
                return Response({'error': f'Currency with name - {self.new_name} already exists'}, status=400)
            if len(self.new_name) > 25 or len(self.new_name) < 3:
                raise ValidationError(CurrencyErrorMessages.WRONG_CURRENCY_NAME_ERROR.value)
        except (Currency.DoesNotExist, ValidationError) as exc:
            if raise_exception:
                raise exc
            return False
        return True

