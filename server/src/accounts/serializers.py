from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'second_name',
            'image'
        ]