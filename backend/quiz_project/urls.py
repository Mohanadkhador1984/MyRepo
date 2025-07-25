# backend/quiz_project/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve as static_serve
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = BASE_DIR / "frontend_build" / "dist"

urlpatterns = [
    # 1) لوحة الإدارة
    path("admin/", admin.site.urls),

    # 2) API التطبيق
    path("api/quiz/", include(("quiz.urls", "quiz"), namespace="quiz")),

    # 3) service-worker.js و offline.html
    re_path(
        r"^service-worker\.js$",
        static_serve,
        {"document_root": DIST_DIR, "path": "service-worker.js"},
    ),
    re_path(
        r"^offline\.html$",
        static_serve,
        {"document_root": DIST_DIR, "path": "offline.html"},
    ),

    # 4) Catch-all: يقدم index.html لتطبيق SPA
    re_path(
        r"^.*$",
        TemplateView.as_view(template_name="index.html"),
        name="spa",
    ),
]
