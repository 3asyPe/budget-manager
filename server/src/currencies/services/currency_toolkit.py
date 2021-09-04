from accounts.models import User, account
from currencies.models import Currency


class CurrencyToolkit:
    # Add sort by user
    @classmethod
    def get_currency(cls, id: str) -> Currency:  
        qs = Currency.objects.filter(id=id, public=True)
        if qs.exists():
            return qs.first()
        
        qs = Currency.objects.filter(id=id, public=False, account=User.account)
        if qs.exists():
            return qs.first()
        
        raise Currency.DoesNotExist()

    @classmethod
    def create_currency(cls, name, code, account):
        from currencies.services import CurrencyCreator
        currency = CurrencyCreator(
            name=name,
            code=code,
            account=account
        )()

        return currency

    @classmethod
    def delete_currency(cls, currency_id):
        currency = cls.get_currency(currency_id=currency_id)
        currency.delete()
        return True

    @classmethod
    def edit_currency(cls, id, new_name, new_code):
        from currencies.services import CurrencyEditor
        return CurrencyEditor(
            id=id,
            new_name=new_name,
            new_code=new_code
        )()

    @classmethod
    def get_accounts_currencies(cls, account):
        pass