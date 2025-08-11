from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField('رقم الهاتف', max_length=20, unique=True)

    # نعتمد رقم الهاتف لحقل المصادقة بدلاً من username
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []  # لإنشاء superuser دون طلب حقول إضافية

    def __str__(self):
        return str(self.phone)
