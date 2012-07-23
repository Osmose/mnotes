from django.contrib.auth.models import User

from mnotes.users.models import APIKey


def create_user(email):
    user = User.objects.create_user(email, email)
    APIKey.objects.create(user=user)
    return user
