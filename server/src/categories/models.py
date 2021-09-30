from django.db import models


class category(models.Model):
    name = models.CharField(max_length=35)
    is_hidden = models.BooleanField(default=False)

    class Meta:
        abstract = True