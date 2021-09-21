import coreapi
from rest_framework.schemas import AutoSchema


class CurrencyViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post', 'put']:
            extra_fields = [
                coreapi.Field('name'),
                coreapi.Field('code')
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields