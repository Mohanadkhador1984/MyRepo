"""
WSGI config for quiz_project project.
Ensures Django + WhiteNoise serve PWA root files & static assets.
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# يجب تثبيت whitenoise في env
from whitenoise import WhiteNoise

# تعيين إعدادات Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')

# إنشاء تطبيق WSGI
application = get_wsgi_application()

# إعداد WhiteNoise ليخدم root-level files من DIST_DIR
BASE_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = BASE_DIR / 'frontend_build' / 'dist'

application = WhiteNoise(
    application,
    root=str(DIST_DIR),
    prefix='',
    autorefresh=True  # يفيد في التطوير
)
