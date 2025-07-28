# backend/quiz_project/urls.py

import os
from pathlib import Path

from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from quiz.views import FrontendAppView


# تأكد من أن settings.py يحوي:
# TEMPLATES[0]["DIRS"] = [ str(DIST_DIR), … ]
# STATICFILES_DIRS = [ str(DIST_DIR), … ]
# و WhiteNoise مُفعّل لخدمة الملفات الثابتة.

urlpatterns = [
    # 1) لوحة الإدارة
    path("admin/", admin.site.urls),
     path('', FrontendAppView.as_view()),

    # 2) API التطبيق
    path("api/quiz/", include(("quiz.urls", "quiz"), namespace="quiz")),

    # 3) ملفات PWA الرئيسيّة (يُخدَم كلٌّ منها من مجلد dist)
    path(
        "service-worker.js",
        TemplateView.as_view(
            template_name="service-worker.js",
            content_type="application/javascript",
        ),
        name="service-worker",
    ),
    path(
        "offline.html",
        TemplateView.as_view(
            template_name="offline.html",
            content_type="text/html",
        ),
        name="offline",
    ),
    path(
        "manifest.json",
        TemplateView.as_view(
            template_name="manifest.json",
            content_type="application/json",
        ),
        name="manifest",
    ),
    path(
        "favicon.ico",
        TemplateView.as_view(
            template_name="favicon.ico",
            content_type="image/x-icon",
        ),
        name="favicon",
    ),

    # 4) كل مسار آخر → index.html لتطبيق الـ SPA
    re_path(
        r"^.*$",
        TemplateView.as_view(template_name="index.html"),
        name="spa",
    ),
    # ملفات PWA
    re_path(
        r"^(?P<path>service-worker\.js|offline\.html|manifest\.json|favicon\.ico)$",
        TemplateView.as_view(template_name=r"%(path)s"),
        name="pwa-static",
    ),

    # كل شيء آخر → index.html لتطبيق الـ SPA
    re_path(r"^.*$", TemplateView.as_view(template_name="index.html"), name="spa"),

    
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


