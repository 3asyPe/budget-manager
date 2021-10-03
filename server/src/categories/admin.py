from django.contrib import admin

from categories.models import IncomeCategory, ExpenseCategory, ComissionCategory


admin.site.register(IncomeCategory)
admin.site.register(ExpenseCategory)
admin.site.register(ComissionCategory)


