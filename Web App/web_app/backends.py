from django.contrib.auth.backends import ModelBackend
from .models import Mirror_Users

class UIDAuthenticationBackend(ModelBackend):
    def authenticate(self, request, uid=None, password=None, **kwargs):
        try:
            user = Mirror_Users.objects.get(uid=uid)
            if user.check_password(password):
                return user
            else:
                return None
        except Mirror_Users.DoesNotExist:
            return None
