from rest_framework import schemas
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from currencies.api.serializers import CurrencySerializer
from currencies.models import Currency
from currencies.services import CurrencyToolkit
from app.errors import ObjectAlreadyExists, ValidationError
from app.utils import AppErrorMessages
from currencies.utils import CurrencyErrorMessages


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
        CurrencyToolkit.delete_currency(currency_id=id, account=request.user.account)
    except Currency.DoesNotExist:
        return Response({"error": CurrencyErrorMessages.CURRENCY_DOES_NOT_EXIST_ERROR.value}, status=404)

    return Response(status=204)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_currency_api(request, id):
    try:
        currency = CurrencyToolkit.get_currency_by_id(user=request.user, id=id)
    except Currency.DoesNotExist:
        return Response({"error" : CurrencyErrorMessages.CURRENCY_DOES_NOT_EXIST_ERROR.value}, status=404)

    serializer = CurrencySerializer(instance=currency)
    return Response(serializer.data, status=200)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_currency_api(request, id):
    data = request.POST or request.data

    try:
        new_name = data['new_name']
        new_code = data['new_code'] 
    except KeyError:
        return Response({"error" : AppErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)
    
    try:
        currency = CurrencyToolkit.edit_currency(
            id=id,
            new_code=new_code,
            new_name=new_name,
            account=request.user.account
         )
    except ValidationError as exc:
        return Response({"error" : str(exc)}, status=400)
    except ObjectAlreadyExists:
        return Response({"error" : CurrencyErrorMessages.CURRENCY_ALREADY_EXISTS_ERROR.value}, status=400)
    except Currency.DoesNotExist:
        return Response({"error" : CurrencyErrorMessages.CURRENCY_DOES_NOT_EXIST_ERROR.value}, status=404)

    serializer = CurrencySerializer(instance=currency)
    return Response(serializer.data, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_currencies_by_account_api(request):
    currencies = Currency.objects.filter(account=request.user.account)
    
    serializer = CurrencySerializer(instance=currencies, many=True)
    return Response(serializer.data, status=200)