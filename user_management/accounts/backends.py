from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User as AuthUser
from .models import User

class UserTypeBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, user_type=None, **kwargs):
        try:
            user = User.objects.get(username=username, user_type=user_type)
        except User.DoesNotExist:
            return None
        if password is not None and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None