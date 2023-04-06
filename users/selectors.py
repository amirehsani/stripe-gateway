""" Selectors are functions that mostly take care of fetching from the database. """

from .models import Profile, BaseUser


def get_profile(user: BaseUser) -> Profile:
    return Profile.objects.get(user=user)
