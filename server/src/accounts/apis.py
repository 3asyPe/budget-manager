from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework.response import Response
import accounts
from accounts import serializers

from accounts.models import User
from accounts.services import UserCreator, UserToolKit
from accounts.serializers import UserSerializer
from app.errors import ValidationError
from app.errors import ObjectAlreadyExists
from rest_framework.authtoken.models import Token


@api_view(["POST"])
def create_user_api(request, *args, **kwargs):
    data = request.POST or request.data

    username = data.get('username')
    first_name = data.get('first_name')
    second_name = data.get('second_name')
    password = data.get('password')

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
 