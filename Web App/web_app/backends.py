from django.contrib.auth.backends import BaseBackend, ModelBackend
from web_app.models import *
from django.contrib.auth import get_user_model

class MirrorUsersBackend(BaseBackend):
    def authenticate(self, request, uid=None, password=None):
        User = get_user_model()
        print("inside custom auth")
        try:
            user = User.objects.get(uid=uid)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, uid):
        User = get_user_model()
        try:
            return User.objects.get(uid=uid)
        except User.DoesNotExist:
            return None
