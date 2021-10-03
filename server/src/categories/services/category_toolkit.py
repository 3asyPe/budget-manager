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
    def create_expense_category(cls, name, is_hidden, parent):
        from categories.services import ExpenseCategoryCreator
        expence_category = ExpenseCategoryCreator(
            name=name,
            is_hidden=is_hidden,
            parent=parent
        )()

        return expence_category

    @classmethod
    def create_comission_category(cls, name, is_hidden, parent):
        from categories.services import ComissionCategoryCreator
        comission_category = ComissionCategoryCreator(
            name=name,
            is_hidden=is_hidden,
            parent=parent
        )()

        return comission_category