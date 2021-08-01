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
        start_balance = data["start_balance"]
        currency_name = data["currency_name"]
    except KeyError:
        return Response({"error": AppErrorMessages.REQUEST_FIELDS_ERROR.value}, 400)

    try:
        wallet = WalletToolkit.create_wallet(
            user=request.user,
            name=name,
            start_balance=start_balance,
            currency_name=currency_name
        )
    except ValidationError as exc:
        return Response({"error": str(exc.value)}, 400)
    except ObjectAlreadyExists:
        return Response({"error": AppErrorMessages.OBJECT_ALREADY_EXISTS_ERROR.value}, 400)
    except Currency.DoesNotExist:
        return Response({"error", CurrencyErrorMessages.CURRENCY_DOES_NOT_EXIST_ERROR.value}, 404)

    serializer = WalletSerializer(instance=wallet)
    return Response(serializer.data, 201)
    