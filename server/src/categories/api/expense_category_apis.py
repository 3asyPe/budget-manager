from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app.errors import ValidationError

from categories.api.serializers import CategorySerializer
from app.utils import AppErrorMessages
from categories.services.category_toolkit import CategoryToolkit


@api_view(["POST"])
def create_income_category_api(request):
    data = request.POST or request.data

    try:
        name = data['name']
        is_hidden = data['hidden']
        parent = data['parent']
    except KeyError:
        return Response({"error": AppErrorMessages})

    try:
        income_category = CategoryToolkit.create_income_category(
            name=name,
            is_hidden=is_hidden,
            parent=parent
        )
    except ValidationError as exc:
        return Response({"error": str(exc)}, status=400)

    serializer = CategorySerializer(instance=income_category)
    return Response(serializer.data, status=210)