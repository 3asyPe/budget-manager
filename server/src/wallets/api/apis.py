from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.errors import ValidationError, ObjectAlreadyExists
from app.utils import AppErrorMessages
from currencies.models import Currency
from currencies.utils import CurrencyErrorMessages
from wallets.api.serializers import WalletSerializer
from wallets.services import WalletToolkit


@api_view(["POST"])
def create_wallet_api(request):
    data = request.POST

    try:
        name = data["name"]
        balances = data["balances"]
    except KeyError:
        return Response({"error": AppErrorMessages.REQUEST_FIELDS_ERROR.value}, 400)

    try:
        wallet = WalletToolkit.create_wallet(
            user=request.user,
            name=name,
            balances=balances,
        )
    except ValidationError as exc:
        return Response({"error": str(exc.value)}, 400)
    except ObjectAlreadyExists:
        return Response({"error": AppErrorMessages.OBJECT_ALREADY_EXISTS_ERROR.value}, 400)
    except Currency.DoesNotExist:
        return Response({"error", CurrencyErrorMessages.CURRENCY_DOES_NOT_EXIST_ERROR.value}, 404)

    serializer = WalletSerializer(instance=wallet)
    return Response(serializer.data, 201)


@api_view(["PUT"])
def edit_wallet_api(request):
    data = request.POST

    try:
        id = data["id"]
        name = data["name"]
        balances = data["balances"]
    except KeyError;
        return Response({"error": AppErrorMessages.REQUEST_FIELDS_ERROR.value}, 400)
    

        