from django.db import models


class WalletBalance(models.Model):
    wallet = models.ForeignKey("wallets.Wallet", on_delete=models.CASCADE, related_name="balances")
    currency = models.ForeignKey("currencies.Currency", on_delete=models.CASCADE, related_name="balances")
    amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = ("Wallet balance")
        verbose_name_plural = ("Wallet balances")

    def __str__(self):
        return f"{self.amount} {self.currency.name}"