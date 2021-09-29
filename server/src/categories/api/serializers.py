from rest_framework import serializers

from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category;
        fields = [
            'id',
            'name',
            'is_hidden',
            'parent',
        ]

        def get_parrent(self, obj):
            parent = obj.parent
            return parent
