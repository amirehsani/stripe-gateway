""" Selectors are functions that mostly take care of fetching from the database. """

from django.db.models import QuerySet

from .models import Profile, BaseUser


def get_profile(user: BaseUser) -> QuerySet[Profile]:
    return Profile.objects.get(user=user)