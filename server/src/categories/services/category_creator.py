from accounts import models
from app.errors import ValidationError
from categories.models import Category, IncomeCategory, ComissionCategory, ExpenseCategory
from categories.utils import CategoryErrorMessages


class CategoryCreator:
    def __init__(self, name: str, is_hidden: bool, parent: models, id: int):
        self.name = name
        self.is_hidden = is_hidden
        self.parent = parent
        self.id = id

    def __call__(self, raise_exception=True):
        if self.allowed_to_create(raise_exception):
            return self.create()
        else:
            return None

    def allowed_to_create(self, raise_exception=True):
        try:
            if 3 > len(self.name) > 25:
                raise ValidationError(CategoryErrorMessages.WRONG_CATEGORY_NAME_ERROR.value)
        except ValidationError as exc:
            if raise_exception:
                raise exc
            else:
                return False

    class Meta:
        abstract = True


class IncomeCategoryCreator(CategoryCreator):
    def create_income_category(self, name, is_hidden, parent):
        return IncomeCategory.objects.create(
            name=name,
            is_hidden = is_hidden,
            parent=parent,
        )


class ExpenseCategoryCreator(CategoryCreator):
    def create_expense_category(self, name, is_hidden, parent):
        return ExpenseCategory.objects.create(
            name,
            is_hidden,
            parent
        )


class ComissionCategoryCreator(CategoryCreator):
    def create_comission_category(self, name, is_hidden, parent):
        return ComissionCategory.objects.create(
            name,
            is_hidden,
            parent
        )