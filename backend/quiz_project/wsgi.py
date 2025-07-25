"""
WSGI config for quiz_project project.
يضمن Django + WhiteNoise خدمة ملفات PWA الثابتة والـ SPA index.html.
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# تعيين إعدادات Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')

# إنشاء تطبيق WSGI الأساسي
application = get_wsgi_application()

# مسار مجلد البناء النهائي للـ frontend
BASE_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = BASE_DIR / 'frontend_build' / 'dist'

# تفعيل WhiteNoise
application = WhiteNoise(
    application,
    root=str(DIST_DIR),
    prefix='',               # بدون بادئة، يخدم مجانا على الجذر
    index_file=True,         # يعيد index.html لأي مسار غير معروف (SPA)
    autorefresh=False,       # فقط للتطوير يمكنك تفعيله عبر DEBUG
    max_age=86400,           # زمن التخزين المؤقت للتحكم في الكاش
)

# إضافة ملفات ثابتة إضافية إن لزم
# application.add_files(str(DIST_DIR / 'static'), prefix='static/')
