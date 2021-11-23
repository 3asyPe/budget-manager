from accounts.models import User, Account
from currencies.models import Currency


class CurrencyToolkit:
    @classmethod
    def get_currency_by_name(cls, user: User, name: str) -> Currency:  
        qs = Currency.objects.filter(name=name, public=True)
        if qs.exists():
            return qs.first()
        
        qs = Currency.objects.filter(name=name, public=False, account=user.account)
        if qs.exists():
            return qs.first()
        
        raise Currency.DoesNotExist()


    @classmethod
    def get_currency_by_id(cls, user: User, id: int) -> Currency:
        qs = Currency.objects.filter(id=id, public=True)
        if qs.exists():
            return qs.first()

        qs = Currency.objects.filter(id=id, public=False, account=user.account)
        if qs.exists():
            return qs.first()
        
        raise Currency.DoesNotExist()


    @classmethod
    def create_currency(cls, name: str, code: str, account: Account):
        from currencies.services import CurrencyCreator
        currency = CurrencyCreator(
            name=name,
            code=code,
            account=account
        )()

        return currency

    @classmethod
    def delete_currency(cls, currency_id: int, account: Account):
        currency = Currency.objects.get(id=currency_id, public=False, account=account)
        currency.delete()
        return True


    @classmethod
    def edit_currency(cls, id: int, new_name: str, new_code: str, account: Account):
        from currencies.services import CurrencyEditor
        if Currency.objects.filter(id=id, public=False, account=account).exists():
            return CurrencyEditor(
                id=id,
                new_name=new_name,
                new_code=new_code
            )()
        else:
            raise Currency.DoesNotExist()