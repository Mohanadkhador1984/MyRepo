# backend/quiz_project/wsgi.py

import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

import os, sys
sys.path.insert(0, os.path.dirname(__file__))  # يضيف مجلد backend


# 1) تعريف BASE_DIR (المجلد الذي يحتوي على manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# 2) تهيئة بيئة Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz_project.settings")
application = get_wsgi_application()

# 3) تغليف التطبيق بخدمة WhiteNoise للستاتيك
application = WhiteNoise(
    application,
    root=str(BASE_DIR / "staticfiles"),  # يتطابق مع STATIC_ROOT
    prefix="static/"                      # يطابق STATIC_URL بدون الشرطة الختامية
)
