from django.db import models
from common.models import BaseModel
from users.models import BaseUser


class UserPayment(BaseModel):
    user = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING, related_name='user_payment')
    payment_status = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=300, null=False, blank=Fasle)  # what is this?
