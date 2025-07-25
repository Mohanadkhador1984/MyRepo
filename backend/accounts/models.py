from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # احذف هذا السطر نهائياً:
    # password = models.CharField(max_length=128),

    # احتفظ فقط بالحقل الإضافي الذي تريده
    is_verified = models.BooleanField(default=False)
