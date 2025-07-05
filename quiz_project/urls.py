"""
URL configuration for quiz_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from quiz.views import offline  # تأكد أن لديك هذا الـ view في quiz/views.py
import os
urlpatterns = [
    # لوحة التحكم
    path('admin/', admin.site.urls),

    # التطبيق الأساسي (تسجيل الدخول، تسجيل حساب، الصفحة الرئيسية)
    path('', include('account.urls')),

    # تطبيق الكويز (quiz)
    path('quiz/', include(('quiz.urls', 'quiz'), namespace='quiz')),

    # صفحة عدم الاتصال
    path('offline.html', offline, name='offline'),

    # ملفات PWA: service worker و manifest
    re_path(r'^manifest.json$', serve, {'path': os.path.join(settings.BASE_DIR, 'static/pwa/manifest.json')}),
    re_path(r'^serviceworker.js$', serve, {'path': os.path.join(settings.BASE_DIR, 'static/pwa/serviceworker.js')}),
]

# إضافة مسارات الملفات الثابتة أثناء وضع التطوير
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)