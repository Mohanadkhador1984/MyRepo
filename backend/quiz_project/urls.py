# project/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve as static_serve
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = BASE_DIR / 'frontend_build' / 'dist'

urlpatterns = [
    # 1) لوحة الإدارة
    path('admin/', admin.site.urls),

    # 2) API التطبيق
    path('api/quiz/', include(('quiz.urls', 'quiz'), namespace='quiz')),

    # 3) service-worker.js و offline.html
    re_path(r'^(service-worker\.js|offline\.html)$', static_serve, {
        'document_root': DIST_DIR,
        'path': lambda m: m.group(1)
    }),

    # 4) كل شيء آخر → يقدم index.html من مجلد الـ SPA
    re_path(r'^(?:.*)/?$', static_serve, {
        'document_root': DIST_DIR,
        'path': 'index.html'
    }),
]
