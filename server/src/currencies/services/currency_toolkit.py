from accounts.models import User, account
from currencies.models import Currency


class CurrencyToolkit:
    # Add sort by user
    @classmethod
    def get_currency(cls, user: User, name: str) -> Currency:  
        qs = Currency.objects.filter(name=name, public=True)
        if qs.exists():
            return qs.first()
        
        qs = Currency.objects.filter(name=name, public=False, account=user.account)
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