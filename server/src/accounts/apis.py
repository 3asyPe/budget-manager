from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.services import UserToolKit
from accounts.serializers import UserSerializer
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
        user = UserToolKit.creater_user(
            username,
            first_name,
            second_name,
            password
        )
    except ObjectAlreadyExists:
        return Response({'error': f'User {username} already exists'}, status=400)

    serializers = UserSerializer(instance=user)
    return Response(serializers.data, status=200)


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
        return Response({'error': str(exc.value)}, status=400)

    serializers = UserSerializer(instance=user)
    return Response(serializers.data, status=200)
 