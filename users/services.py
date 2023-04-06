""" Services are functions that mostly take care of writing to the database. """

from django.db import transaction

from .models import BaseUser, Profile


def create_profile(*, user: BaseUser, country: str) -> Profile:
    return Profile.objects.create(user=user, country=country)


def create_user(*, email: str, password: str) -> BaseUser:
    return BaseUser.objects.create_user(email=email, password=password)


# Undo all the process in case of failure or malfunction
@transaction.atomic()
def register(*, country: str, email: str, password: str) -> BaseUser:

    user = create_user(email=email, password=password)
    create_profile(user=user, country=country)

    return user
