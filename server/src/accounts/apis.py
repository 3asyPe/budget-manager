from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.services import UserToolKit
from accounts.serializers import UserSerializer, AccountSerializer
from accounts.utils import AccountErrorMessages
from app.errors import ValidationError, ObjectAlreadyExists
from app.utils import AppErrorMessages


@api_view(["POST"])
def create_user_api(request, *args, **kwargs):
    data = request.POST or request.data

    try:
        username = data['username']
        first_name = data['first_name']
        second_name = data['second_name']
        password = data['password']
    except KeyError:
        return Response({'error': AppErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)

    try:
        user = UserToolKit.create_user(
            username,
            first_name,
            second_name,
            password
        )
    except ValidationError as exc:
        return Response({'error': str(exc)}, status=400)
    except ObjectAlreadyExists:
        return Response({'error': AccountErrorMessages.NON_UNIQUE_EMAIL_ERROR.value}, status=400)

    serializer = UserSerializer(instance=user)
    return Response(serializer.data, status=201)


@api_view(["POST"])
def authenticate_user_api(request, *args, **kwargs):
    data = request.POST or request.data

    username = data.get('username')
    password = data.get('password')

    try:
        user, token = UserToolKit.authenticate_user(
            username,
            password,
        )
    except ValidationError as exc:
        return Response({'error': str(exc)}, status=400)

    serializer = UserSerializer(instance=user)
    return Response(serializer.data, status=200)
 

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_account_info_api(request, *args, **kwargs):
    account = request.user.account
    serializer = AccountSerializer(instance=account)
    return Response(serializer.data, status=200)
