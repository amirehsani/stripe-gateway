from django.contrib.auth import get_user_model
from users.models import Profile
from users.selectors import get_profile


User = get_user_model()


def test_get_profile():
    # Create a user and profile
    user = User.objects.create_user(email='test@example.com', password='password')
    profile = Profile.objects.create(user=user, country='US')

    # Call get_profile with the user and check that it returns the correct profile
    assert get_profile(user) == profile
