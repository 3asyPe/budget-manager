from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from categories.api.serializers import CategorySerializer
from categories.models import IncomeCategory, ExpenseCategory, ComissionCategory
from app.utils import AppErrorMessages


@api_view(["POST"])
def create_currency_api(request):
    data = request.POST or request.data

    try:
        name = data['name']
        is_hidden = data['hidden']
        parent = data['parent']
    except KeyError:
        return Response({"error": AppErrorMessages})
