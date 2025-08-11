from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("api/quiz/", include(("quiz.urls", "quiz"), namespace="quiz")),

    # أي مسار آخر يُعيد index.html من dist
    re_path(
        r"^(?!static/|media/|api/|admin/).*",
        TemplateView.as_view(template_name="index.html"),
        name="spa-entry",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
