from accounts.models import User
from currencies.models import Currency


class CurrencyToolkit:
    # Add sort by user
    @classmethod
    def get_currency(cls, user: User, currency_name: str) -> Currency:  
        qs = Currency.objects.filter(name=currency_name)
        if qs.exists():
            return qs.first()
        
        raise Currency.DoesNotExist()