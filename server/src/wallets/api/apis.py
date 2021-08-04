from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.errors import ValidationError, ObjectAlreadyExists
from app.utils import AppErrorMessages
from currencies.models import Currency
from currencies.utils import CurrencyErrorMessages
from wallets.api.serializers import WalletSerializer
from wallets.models import Wallet
from wallets.services import WalletToolkit
from wallets.utils import WalletErrorMessages


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
def edit_wallet_api(request, id):
    data = request.PUT

    try:
        name = data["name"]
        balances = data["balances"]
    except KeyError:
        return Response({"error": AppErrorMessages.REQUEST_FIELDS_ERROR.value}, 400)

    try:
        wallet = WalletToolkit.edit_wallet(
            wallet_id=id,
            user=request.user,
            name=name,
            balances=balances,
        )
    except ValidationError as exc:
        return Response({"error": str(exc.value)}, 400)
    except Wallet.DoesNotExist:
        return Response({"error": WalletErrorMessages.WALLET_DOES_NOT_EXIST_ERROR.value}, 404)
    except Currency.DoesNotExist:
        return Response({"error": CurrencyErrorMessages.CURRENCY_DOES_NOT_EXIST_ERROR.value}, 404)

    serializer = WalletSerializer(instance=wallet)
    return Response(serializer.data, 200)


@api_view(["DELETE"])
def delete_wallet_api(request, id):
    try:
        WalletToolkit.delete_wallet(wallet_id=id)
    except Wallet.DoesNotExist:
        return Response({"error": WalletErrorMessages.WALLET_DOES_NOT_EXIST_ERROR.value}, 404)
    
    return Response({}, 204)


@api_view(["GET"])
def get_wallet_api(request, id):
    try:
        wallet = WalletToolkit.get_wallet(wallet_id=id)
    except Wallet.DoesNotExist:
        return Response({"error": WalletErrorMessages.WALLET_DOES_NOT_EXIST_ERROR.value}, 404)

    serializer = WalletSerializer(instance=wallet)
    return Response({}, 200)


@api_view(["GET"])
def get_user_wallets_api(request):
    data = request.GET
    show_hidden = data.get("show_hidden", False)

    wallets = WalletToolkit.get_wallets_by_user(user=request.user, show_hidden=show_hidden)

    serializer = WalletSerializer(many=True, instance=wallets)
    return Response(serializer.data, 200)
