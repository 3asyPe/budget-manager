from categories.models import ComissionCategory, ExpenseCategory, IncomeCategory
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app.errors import ValidationError

from categories.api.serializers import CategorySerializer
from app.utils import AppErrorMessages
from categories.services.category_toolkit import CategoryToolkit
from categories.utils import CategoryErrorMessages


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

@api_view(["DELETE"])
def delete_income_category_api(request, id):
    try:
        CategoryToolkit.delete_income_category(id=id)
    except IncomeCategory.DoesNotExist:
        return Response({"error": CategoryErrorMessages.CATEOGRY_DOES_NOT_EXISTS_ERROR.value}, status=400)

    return Response({'success': f'income category with id - {id} deleted'})
    

@api_view(["POST"])
def create_expense_category_api(request):
    data = request.DATA or request.data

    try:
        name = data['name']
        is_hidden = data['hidden']
        parent = data['parent']
    except KeyError:
        return Response({"error": AppErrorMessages}, status=400)

    try:
        expoense_category = CategoryToolkit.create_expense_category(
            name=name,
            is_hidden=is_hidden,
            parent=parent
        )
    except ValidationError as exc:
        return Response({"error": str(exc)}, status=400)

    serializer = CategorySerializer(instance=expoense_category)
    return Response(serializer.data, status=210)

@api_view(["DELETE"])
def delete_expense_cateogry_api(request, id):
    try:
        CategoryToolkit.delete_expense_cateogry(id=id)
    except ExpenseCategory.DoesNotExist:
        return Response({"error": f"category with id {id} does not exists"})
    return Response({"success": f"expense comission with id - {id} deleted"})

@api_view(["POST"])
def create_comission_category_api(request):
    data = request.DATA or request.data

    try:
        name = data['name']
        is_hidden = data['hidden']
        parent = data['parent']
    except KeyError:
        return Response({"error": AppErrorMessages}, status=400)

    try:
        comission_cateogry = CategoryToolkit.create_comission_category(
            name=name,
            is_hidden=is_hidden,
            parent=parent
        )
    except ValidationError as exc:
        return Response({"error": str(exc)}, status=400)

    serializer = CategorySerializer(instance=comission_cateogry)
    return Response(serializer.data, status=210)

@api_view(["POST"])
def create_income_category_api(request):
    data = request.DATA or request.data

    try:
        name = data['name']
        is_hidden = data['hidden']
        parent = data['parent']
    except KeyError:
        return Response({"error": AppErrorMessages}, status=400)

    try:
        income_cateogry = CategoryToolkit.create_income_category(
            name=name,
            is_hidden=is_hidden,
            parent=parent
        )
    except ValidationError as exc:
        return Response({"error": str(exc)}, status=400)

    serializer = CategorySerializer(instance=income_cateogry)
    return Response(serializer.data, status=210)

@api_view(["DELETE"])
def delete_comission_category_api(request, id):
    try:
        CategoryToolkit.delete_commission_category(id=id)
    except ComissionCategory.DoesNotExist:
        return Response({"error": CategoryErrorMessages.CATEOGRY_DOES_NOT_EXISTS_ERROR.value}, status=400)
    return Response({"success": f"comission cateogry with id - {id} deleted"})