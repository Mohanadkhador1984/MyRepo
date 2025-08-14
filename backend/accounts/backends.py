from django.contrib.auth.backends import BaseBackend
from .models import User

class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None
        return user if user.check_password(password) else None
