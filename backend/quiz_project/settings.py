import os
from pathlib import Path
import environ

# ─── 1. المسارات الأساسية ─────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = BASE_DIR / "frontend_build" / "dist"  # مجلد SPA النهائي (مثل Vue/React)

# ─── 2. تحميل إعدادات البيئة من ملف .env ──────────────────────────────────────
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    USE_REMOTE_DB=(bool, False),
)

environ.Env.read_env(BASE_DIR / ".env")

# ─── 3. الأمان والتصحيح ───────────────────────────────────────────────────────
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# ─── 4. التطبيقات المثبتة ─────────────────────────────────────────────────────
INSTALLED_APPS = [
    # تطبيقات Django الأساسية
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # تطبيقاتك
    "quiz",
    "accounts",

    # تطبيقات خارجية
    "rest_framework",
    "corsheaders",
]

# ─── 5. الوسيطات (Middleware) ─────────────────────────────────────────────────
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # لخدمة الملفات الثابتة
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ─── 6. عنوان التوجيه وملف WSGI ───────────────────────────────────────────────
ROOT_URLCONF = "quiz_project.urls"
WSGI_APPLICATION = "quiz_project.wsgi.application"

# ─── 7. إعدادات القوالب (Templates) ───────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [DIST_DIR],  # لخدمة index.html الخاص بـ SPA
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ─── 8. إعداد قاعدة البيانات ─────────────────────────────────────────────────
USE_REMOTE_DB = env.bool("USE_REMOTE_DB", default=False)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME") if USE_REMOTE_DB else env("DB_NAME_LOCAL"),
        "USER": env("DB_USER") if USE_REMOTE_DB else env("DB_USER_LOCAL"),
        "PASSWORD": env("DB_PASSWORD") if USE_REMOTE_DB else env("DB_PASSWORD_LOCAL"),
        "HOST": env("DB_HOST_EXTERNAL") if USE_REMOTE_DB else env("DB_HOST_LOCAL"),
        "PORT": env.int("DB_PORT") if USE_REMOTE_DB else env.int("DB_PORT_LOCAL", default=5432),
        "OPTIONS": {
            "sslmode": "require" if USE_REMOTE_DB else "disable",
        },
    }
}

# ─── 9. نموذج المستخدم المخصص ────────────────────────────────────────────────
AUTH_USER_MODEL = "accounts.CustomUser"

# ─── 10. التحقق من كلمات المرور ──────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─── 11. اللغة والتوقيت ──────────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ─── 12. الملفات الثابتة (Static Files) ───────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    DIST_DIR,  # يحتوي على ملفات JS/CSS الخاصة بالـ SPA
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ─── 13. إعدادات CORS ────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=["http://localhost:8080"])

# ─── 14. إعدادات Django REST Framework ───────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}

# ─── 15. الإعداد الافتراضي لحقل المفتاح الأساسي ─────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"