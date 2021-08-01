from django.db import models


class Wallet(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    
    is_hidden = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def main_balance(self):
        return self.balances.order_by("created").first()

    def __str__(self):
        return f"{self.user.__str__()} {self.name} Wallet"
