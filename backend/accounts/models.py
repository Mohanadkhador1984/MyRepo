import uuid, secrets
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

def gen_device_code():
    return secrets.token_urlsafe(6)  # مثال: رموز مكوّنة من 6 حروف/أرقام

class CustomUser(AbstractUser):
    phone = models.CharField('رقم الهاتف', max_length=20, unique=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.phone

class Device(models.Model):
    device_id = models.UUIDField(
        'معرّف الجهاز', default=uuid.uuid4, unique=True, editable=False
    )
    code      = models.CharField('رمز التفعيل', max_length=12,
                                 unique=True, default=gen_device_code)
    is_active = models.BooleanField('نشط', default=False)
    user      = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='devices')
    created   = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.phone} — {self.device_id}"
