from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=35)
    is_hidden = models.BooleanField(default=False)

    class Meta:
        abstract = True


