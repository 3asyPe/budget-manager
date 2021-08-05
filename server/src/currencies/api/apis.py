from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import account

from currencies.api.serializers import CurrencySerializer
from currencies.services import CurrencyToolkit
from app.errors import ObjectAlreadyExists, ValidationError
from app.utils import AppErrorMessages
from currencies.models import Currency
from currencies.utils import CurrencyErrorMessages


@api_view(["POST"])
def create_currency_api(request):
    data = request.POST or request.data
    try:
        name = data['name']
        code = data['code']
        account = request.user.account
    except KeyError:
        return Response({"error": AppErrorMessages.REQUEST_FIELDS_ERROR.value}, 400)

    try:
        currency = CurrencyToolkit.create_currency(
            name=name,
            code=code,
            account=account
        )
    except ObjectAlreadyExists:
        return Response({'error': CurrencyErrorMessages.CURRENCY_ALREADY_EXISTS_ERROR.value}, status=400)
    except ValidationError as exc:
        return Response({'error': str(exc)}, status=400)
    serializer = CurrencySerializer(instance=currency)
    return Response(serializer.data, status=200)
