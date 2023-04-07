from django.db import transaction, IntegrityError
from django.contrib.auth import get_user_model
from users.models import Profile
from users.services import create_user, create_profile, register


User = get_user_model()


def test_create_user():
    user = create_user(email='test@example.com', password='password')
    assert User.objects.filter(email='test@example.com').exists()
    assert user.check_password('password') is True


def test_create_profile():
    user = create_user(email='test@example.com', password='password')
    profile = create_profile(user=user, country='US')
    assert Profile.objects.filter(user=user, country='US').exists()
    assert profile.user == user


def test_register():
    with transaction.atomic():
        user = register(email='test@example.com', password='password', country='US')
    assert User.objects.filter(email='test@example.com').exists()
    assert Profile.objects.filter(user=user, country='US').exists()


def test_register_failure():
    with transaction.atomic():
        # Use an existing email to trigger a failure
        user = register(email='test@example.com', password='password', country='US')
        try:
            register(email='test@example.com', password='password', country='CA')
        except IntegrityError:
            pass
    # Make sure the first registration succeeded but the second failed and both rolled back
    assert User.objects.filter(email='test@example.com').count() == 1
    assert Profile.objects.filter(user=user, country='US').exists() is False
