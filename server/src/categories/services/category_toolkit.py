from categories.models import IncomeCategory, ExpenseCategory, ComissionCategory


class CategoryToolkit:
    @classmethod
    def create_income_category(cls, name, is_hidden, parent):
        from categories.services import IncomeCategoryCreator
        income_category = IncomeCategoryCreator(
            name=name,
            is_hidden=is_hidden,
            parent=parent
        )()

        return income_category
    
    @classmethod
    def delete_income_category(cls, id):
        if IncomeCategory.objects.filter(id=id).exists():
            IncomeCategory.objects.filter(id=id).delete()
            return True
        else:
            raise IncomeCategory.DoesNotExist()

    @classmethod
    def create_expense_category(cls, name, is_hidden, parent):
        from categories.services import ExpenseCategoryCreator
        expence_category = ExpenseCategoryCreator(
            name=name,
            is_hidden=is_hidden,
            parent=parent
        )()

        return expence_category

    @classmethod
    def delete_expense_cateogry(cls, id):
        if ExpenseCategory.objects.filter(id=id).exists():
            ExpenseCategory.objects.filter(id=id).delete()
            return True
        else:
            raise ExpenseCategory.DoesNotExist()

    @classmethod
    def create_comission_category(cls, name, is_hidden, parent):
        from categories.services import ComissionCategoryCreator
        comission_category = ComissionCategoryCreator(
            name=name,
            is_hidden=is_hidden,
            parent=parent
        )()

        return comission_category

    @classmethod
    def delete_commission_category(cls, id):
        if ComissionCategory.objects.filter(id=id).exists():
            ComissionCategory.objects.filter(id=id).delete()
            return True
        else:
            raise ComissionCategory.DoesNotExist()