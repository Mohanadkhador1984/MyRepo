import os
from pathlib import Path
from dotenv import load_dotenv

# --------------------------------------------------
# تحميل متغيرات البيئة
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# --------------------------------------------------
# الأمان و التصحيح
# --------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Missing DJANGO_SECRET_KEY in environment")

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    uri.strip()
    for uri in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if uri.strip()
]

# --------------------------------------------------
# اختيار القاعدة: محلي أو بعيد
# --------------------------------------------------
USE_REMOTE_DB = os.getenv("USE_REMOTE_DB", "False").lower() in ("true", "1", "yes")

if USE_REMOTE_DB:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST_EXTERNAL"),   # تأكد من تطابق المفتاح
            "PORT": os.getenv("DB_PORT", "5432"),
            "OPTIONS": {"sslmode": "require"},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": f"django.db.backends.{os.getenv('DATABASE_LOCAL_ENGINE', 'postgresql')}",
            "NAME": os.getenv("DATABASE_LOCAL_NAME", "quizdb"),
            "USER": os.getenv("DATABASE_LOCAL_USER", "postgres"),
            "PASSWORD": os.getenv("DATABASE_LOCAL_PASSWORD", ""),
            "HOST": os.getenv("DATABASE_LOCAL_HOST", "localhost"),
            "PORT": os.getenv("DATABASE_LOCAL_PORT", "5432"),
        }
    }

# --------------------------------------------------
# التطبيقات والوسيطات
# --------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",
    "crispy_forms",
    "crispy_bootstrap4",
    "pwa",
    "quiz",
    "account",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "quiz_project.urls"
WSGI_APPLICATION = "quiz_project.wsgi.application"

# --------------------------------------------------
# القوالب
# --------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ]},
    },
]

# --------------------------------------------------
# الملفات الثابتة وWhiteNoise
# --------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --------------------------------------------------
# المصادقة وإعادة التوجيه
# --------------------------------------------------
LOGIN_REDIRECT_URL = "/home/"
LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "/login/"

# --------------------------------------------------
# إعدادات PWA
# --------------------------------------------------
PWA_APP_NAME = "Quiz App"
PWA_APP_DESCRIPTION = "تطبيق يعمل دون اتصال"
PWA_APP_THEME_COLOR = "#0A0302"
PWA_APP_BACKGROUND_COLOR = "#ffffff"
PWA_APP_DISPLAY = "standalone"
PWA_APP_SCOPE = "/"
PWA_APP_START_URL = "/"
PWA_APP_STATUS_BAR_COLOR = "default"
PWA_APP_ICONS = [
    {"src": "/static/pwa/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "/static/pwa/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
]
PWA_SERVICE_WORKER_PATH = BASE_DIR / "static" / "pwa" / "serviceworker.js"
