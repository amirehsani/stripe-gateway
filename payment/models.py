from django.db import models

from config import settings
from users.models import BaseUser


class Payment(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING, related_name='user_payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    description = models.CharField(max_length=255)
    payment_status = models.BooleanField(default=False)
    stripe_charge_id = models.CharField(max_length=255, null=True, blank=True)

    def charge(self, token):
        import stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            charge = stripe.Charge.create(
                amount=int(self.amount * 100),
                currency=self.currency,
                description=self.description,
                source=token,
            )
            self.stripe_charge_id = charge['id']
            self.save()
            return True
        except stripe.error.CardError as ex:
            return f"Declined! Error: {ex}"
