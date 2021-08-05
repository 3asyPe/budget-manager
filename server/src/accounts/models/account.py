from django.db import models


class Account(models.Model):
    @property
    def owner(self):
        return self.users.filter(owner=True).first()