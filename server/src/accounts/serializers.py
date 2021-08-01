from rest_framework import serializers
from rest_framework.authtoken.models import Token


from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'second_name',
            'image',
            'token',
            'id',
        ]

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key