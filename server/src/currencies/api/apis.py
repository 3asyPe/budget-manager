from django.db.models.query import InstanceCheckMeta
from currencies import services
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import account

from currencies.api.serializers import CurrencySerializer
from currencies.models import Currency
from currencies.services import CurrencyToolkit
from app.errors import ObjectAlreadyExists, ValidationError
from app.utils import AppErrorMessages
from currencies.utils import CurrencyErrorMessages
from currencies.services import CurrencyCreator, CurrencyEditor


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
def delete_currency_api(request, id):
    try:
        CurrencyToolkit.delete_currency(currency_id=id)
    except Currency.DoesNotExist:
        return Response({"error": CurrencyErrorMessages.CURRENCY_DOES_NOT_EXIST_ERROR.value}, 404)
    
    return Response({}, 204)


@api_view(["GET"])
def get_currency_api(request):
    data = request.data
    try:
        name = data['name']
    except KeyError:
        return Response({'error': AppErrorMessages.REQUEST_FIELDS_ERROR.value}, 400)

    try:
        currency = CurrencyToolkit.get_currency(name)
    except:
        return Response({"error": CurrencyErrorMessages.CURRENCY_DOES_NOT_EXIST_ERROR.value}, status=400)

    serializer = CurrencySerializer(instance=currency)
    return Response(serializer.data, status=200)

@api_view(["PUT"])
def edit_currency_api(request):
    data = request.data

    try:
        name = data['name']
        new_name = data['new_name']
        new_code = data['new_code']
    except KeyError:
        return Response({'error': AppErrorMessages.REQUEST_FIELDS_ERROR.value}, 400)

    try:
        CurrencyToolkit.edit_currency(
            name=name,
            new_name=new_name,
            new_code=new_code
        )
        currency = Currency.objects.filter(name=new_name)
    except ValidationError as exc:
        return Response({'errpr': str(exc)}, 400)
    except Currency.DoesNotExist:
        return Response({'error': CurrencyErrorMessages.CURRENCY_DOES_NOT_EXIST_ERROR.value})

    serializer = CurrencySerializer(instance=currency, many=True)
    return Response(serializer.data, status=200)