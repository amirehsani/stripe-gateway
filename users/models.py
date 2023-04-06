from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import BaseUserManager
from common.models import BaseModel


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name="email address", unique=True, blank=False)

    is_admin = models.BooleanField(
        _("admin status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
    )

    objects = BaseUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_admin


class Profile(models.Model):

    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    country = models.CharField(max_length=155, blank=False, null=False)

    def __str__(self):
        return self.user.email
