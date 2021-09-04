from rest_framework import response, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import account

from currencies.api.serializers import CurrencySerializer
from currencies.models import Currency
from currencies.services import CurrencyToolkit
from app.errors import ObjectAlreadyExists, ValidationError
from app.utils import AppErrorMessages
from currencies.utils import CurrencyErrorMessages
from accounts.utils import AccountErrorMessages
from accounts.models import Account


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

@api_view(["DELETE"])
def delete_currency_api(request):
    data = request.POST or request.data

    try:
        id = data['id']
        CurrencyToolkit.delete_currency(currency_id=id)
    except:
        return Response({"error": CurrencyErrorMessages.CURRENCY_DOES_NOT_EXIST_ERROR.value}, status=400)

    return Response({'success': f'currency with id {id} deleted'})

@api_view(["GET"])
def get_currency_api(request):
    data = request.POST or request.data

    try:
        id = data['id']
    except:
        return Response({"error" : CurrencyErrorMessages.CURRENCY_DOES_NOT_EXIST_ERROR.value}, 404)

    currency = CurrencyToolkit.get_currency(id=id)
    serializer = CurrencySerializer(instance=currency)
    return Response(serializer.data, status=200)

@api_view(["PUT"])
def edit_currency_api(request):
    data = request.POST or request.data

    try:
        id = data['id']
        new_name = data['new_name']
        new_code = data['new_code'] 

    except:
        return Response({"error": CurrencyErrorMessages.CURRENCY_DOES_NOT_EXIST_ERROR.value}, status=400)
    
    CurrencyToolkit.edit_currency(
        id=id,
        new_code=new_code,
        new_name=new_name
    )
    currency = Currency.objects.filter(id=id)

    serializer = CurrencySerializer(instance=currency, many=True)
    return Response(serializer.data, status=200)

@api_view(["GET"])
def get_currencies_api(request):
    currencies = Currency.objects.all()

    serializer = CurrencySerializer(instance=currencies, many=True)
    return Response(serializer.data, status=200)

@api_view(["GET"])
def get_accounts_currency_api(request):
    data = request.POST or request.data

    try:
        account_id = data['account_id']

    except:
        return Response({"error": AccountErrorMessages.WRONG_ACCOUNT_ID_ERROR.value}, status=400)
    
    account = Account.objects.get(id=account_id)
    currency = Currency.objects.filter(account=account)
    serializer = CurrencySerializer(instance=currency, many=True)

    return Response(serializer.data, status=200)

    