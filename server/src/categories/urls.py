from django.urls import path

from categories.api import apis


urlpatterns = [
    path('api/income_category/create/', apis.create_income_category_api),
    path('api/comission_cateogry/create/', apis.create_comission_category_api),
    path('api/expense_category/create/', apis.create_comission_category_api),
    path('api/income_category/<int:id>/delete/', apis.delete_income_category_api),
    path('api/comission_category/<int:id>/delete/', apis.delete_comission_category_api),
    path('api/expense_cateogry/<int:id>/delete/', apis.delete_expense_cateogry_api),
]
