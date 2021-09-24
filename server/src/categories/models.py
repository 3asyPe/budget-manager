from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=35)
    is_hidden = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Expense(Category):
    expence = models.FloatField(max_length=34)

    class Meta:
        verbose_name = ("Expense")
        verbose_name_plural = ("Expenses")


class Income(Category):
    income = models.FloatField(max_length=34)

    class Meta:
        verbose_name = ("Income")
        verbose_name_plural = ("Incomes")


class Comission(Category):
    comission = models.FloatField(max_length=34)

    class Meta:
        verbose_name = ("Comission")
        verbose_name_plural = ("Comissions")