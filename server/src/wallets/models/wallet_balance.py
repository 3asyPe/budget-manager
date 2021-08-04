from django.db import models


class WalletBalance(models.Model):
    wallet = models.ForeignKey("wallets.Wallet", on_delete=models.CASCADE, related_name="balances")
    currency = models.ForeignKey("currencies.Currency", on_delete=models.CASCADE, related_name="balances")
    amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    main = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("Wallet balance")
        verbose_name_plural = ("Wallet balances")

    def set_as_main(self, save_instance=True):
        for balance in self.wallet.balances.all():
            if balance.main and balance != self:
                balance.main = False
                balance.save()
        self.main = True
        if save_instance:
           self.save() 

    def __str__(self):
        return f"{self.amount} {self.currency.name}"