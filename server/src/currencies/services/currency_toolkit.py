from accounts.models import User
from currencies.models import Currency


class CurrencyToolkit:
    @classmethod
    def get_currency(cls, user: User, currency_name: str) -> Currency:  
        qs = Currency.objects.filter(user=user, name=currency_name, public=False)
        if qs.exists():
            return qs.first()
        
        qs = Currency.objects.filter(name=currency_name, public=True)
        if qs.exists():
            return qs.first()
        
        raise Currency.DoesNotExist()