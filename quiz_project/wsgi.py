import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings

# تأكد من تعيين متغيّر إعدادات Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz_project.settings")

# احصل على الـ WSGI application
application = get_wsgi_application()

# لفّ التطبيق بWhiteNoise لخدمة ملفات static من STATIC_ROOT
# استخدم STATIC_URL كبادئة لمسارات الـ static
application = WhiteNoise(
    application,
    root=settings.STATIC_ROOT,
    prefix=settings.STATIC_URL
)
