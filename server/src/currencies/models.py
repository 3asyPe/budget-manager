from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=10)
    code = models.CharField(max_length=3, blank=True, null=True)
    public = models.BooleanField(default=False)
    account = models.ForeignKey('accounts.Account', related_name='currencies',null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Currency")
        verbose_name_plural = ("Currencies")

    def __str__(self):
        public = "Public" if self.public else ""
        code = f"({self.code})" if self.code else ""
        return f"{public} {self.name}{code} Currency"
