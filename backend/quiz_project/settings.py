import os
from pathlib import Path
import environ

# ─── 1. تهيئة البيئة ومسارات المشروع ────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    USE_REMOTE_DB=(bool, False),
)
environ.Env.read_env(BASE_DIR / ".env")

# ─── 2. الأمان والدباغ ───────────────────────────────────────────────
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ─── 3. التطبيقات المثبتة ────────────────────────────────────────────
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Project apps
    "quiz",
    "accounts",

    # Third-party
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt.token_blacklist",
]

# ─── 4. الوسيطات (Middleware) ────────────────────────────────────────
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    # استثناء CSRF لمسارات المصادقة
    "accounts.middleware.CsrfExemptApiAuthMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ─── 5. إعدادات Vue وملفات static ────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False  # ← True فقط محلياً

ALLOWED_HOSTS = ['*']  # أو ['.onrender.com']

# ملفات Vue المبنية
# DIST_DIR = BASE_DIR / 'frontend_dist' / 'dist'
DIST_DIR = BASE_DIR / 'frontend_dist' / 'dist'


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    DIST_DIR ,  # ← مجلد static بداخل Vue
]

# WhiteNoise لتقديم static في الإنتاج
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [DIST_DIR],  # index.html من Vue
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

# ─── 6. قواعد البيانات ────────────────────────────────────────────────
if env("USE_REMOTE_DB"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST_EXTERNAL"),
            "PORT": env("DB_PORT", default="5432"),
            "OPTIONS": {"sslmode": "require"},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "quizdb1",
            "USER": "postgres",
            "PASSWORD": "123456",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }

# ─── 7. REST Framework و JWT ──────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# ─── 8. نموذج المستخدم والمصادقة ─────────────────────────────────────
AUTH_USER_MODEL = "accounts.CustomUser"

AUTHENTICATION_BACKENDS = [
    "accounts.backends.PhoneBackend",
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 4},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    # تم تعليق الفاحص الرقمي للسماح بكلمات سر رقمية
    # {
    #     "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    # },
]

# ─── 9. اللغة والتوقيت ────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ─── 10. عنوان التوجيه وملف WSGI ─────────────────────────────────────
ROOT_URLCONF = "quiz_project.urls"
WSGI_APPLICATION = "quiz_project.wsgi.application"

# ─── 11. CORS و CSRF ──────────────────────────────────────────────────
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ["http://localhost:8080"]
CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

# ─── 12. تسجيل الأخطاء ───────────────────────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "ERROR"},
}

# ─── 13. الحقل الافتراضي للموديلات ──────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'accounts.CustomUser'

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
