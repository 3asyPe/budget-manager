from django.db import models
from django.db.models.fields.related import OneToOneField


class Account(models.Model):
    owner=models.OneToOneField('accounts.User', on_delete=models.CASCADE, primary_key=True)
    users=models.ForeignKey('accounts.User', related_name='User', on_delete=models.CASCADE)
    