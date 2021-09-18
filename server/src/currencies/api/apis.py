from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from currencies.api.serializers import CurrencySerializer
from currencies.models import Currency
from currencies.services import CurrencyToolkit
from app.errors import ObjectAlreadyExists, ValidationError
from app.utils import AppErrorMessages
from currencies.utils import CurrencyErrorMessages

from accounts.utils import AccountErrorMessages


@api_view(["POST"])
@permission_classes([IsAuthenticated])
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
    return Response(serializer.data, status=201)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_currency_api(request, id):
    try:
        CurrencyToolkit.delete_currency(currency_id=id)
    except:
        return Response({"error": CurrencyErrorMessages.CURRENCY_DOES_NOT_EXIST_ERROR.value}, status=400)

    return Response({'success': f'currency with id {id} deleted'})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_currency_api(request, id):
    try:
        currency = CurrencyToolkit.get_currency(id=id)
    except ValidationError as exc:
        return Response({"error" : str(exc)}, status=400)

    serializer = CurrencySerializer(instance=currency)
    return Response(serializer.data, status=200)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_currency_api(request):
    data = request.PUT or request.data

    try:
        id = data['id']
        new_name = data['new_name']
        new_code = data['new_code'] 
    except KeyError:
        return Response({"error" : AppErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)
    
    try:
        CurrencyToolkit.edit_currency(
            id=id,
            new_code=new_code,
            new_name=new_name
         )
    except ValidationError as exc:
        return Response({"error" : str(exc)}, status=400)

    currency = Currency.objects.filter(id=id)
    serializer = CurrencySerializer(instance=currency, many=True)
    return Response(serializer.data, status=200)


@api_view(["GET"])
def get_currency_by_account(request):
    try:
        currencies = Currency.objects.filter(account=request.user.account)
    except:
        return Response({"error": AccountErrorMessages.ACCOUNT_DOES_NOT_EXIST_ERROR.value}, status=400)
    
    serializer = CurrencySerializer(instance=currencies, many=True)

    return Response(serializer.data, status=200)