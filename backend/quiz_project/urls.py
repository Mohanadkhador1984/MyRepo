# backend/quiz_project/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView

from quiz.views import FrontendAppView


urlpatterns = [
    # 1) لوحة إدارة Django
    path("admin/", admin.site.urls),

    # 2) API أسئلة المسابقة
    path(
        "api/quiz/",
        include(("quiz.urls", "quiz"), namespace="quiz")
    ),

    # 3) ملفات PWA ثابتة (تُخدَم من مجلد dist تحت STATICFILES_DIRS)
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

    # 4) جميع المسارات الأخرى (غير admin، api، static، media) → تُوجَّه إلى Vue
    re_path(
        r"^(?!static/|media/|api/|admin/).*$",
        FrontendAppView.as_view(),
        name="spa-entry"
    ),
]

# 5) أثناء التطوير: خدمة ملفات static/media عبر Django مباشرةً
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    # إذا كان لديك MEDIA_URL/ROOT:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
