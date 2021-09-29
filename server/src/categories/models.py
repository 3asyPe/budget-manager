from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=35)
    is_hidden = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ExpenseCategory(Category):
    parent = models.ForeignKey(
        'categories.ExpenseCategory',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = ("Expense")
        verbose_name_plural = ("Expenses")


class IncomeCategory(Category):
    parent = models.ForeignKey(
        'categories.IncomeCategory',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = ("Income")
        verbose_name_plural = ("Incomes")


class ComissionCategory(Category):
    parent = models.ForeignKey(
        'categories.ComissionCategory',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = ("Comission")
        verbose_name_plural = ("Comissions")