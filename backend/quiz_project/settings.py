import environ

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False  # ← True فقط محلياً

ALLOWED_HOSTS = ['*']  # أو ['.onrender.com']

# ملفات Vue المبنية
DIST_DIR = BASE_DIR / 'frontend_dist' / 'dist'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    DIST_DIR / 'static',
    os.path.join(BASE_DIR, 'frontend_dist', 'dist', 'quiz', 'sounds'),  # ← مجلد static بداخل Vue
]

# WhiteNoise لتقديم static في الإنتاج
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# دمج index.html كـ template
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [DIST_DIR],  # ← مسار index.html
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# (إذا كنت تحتاج إعادة تعيين DIRS لاحقًا، ليس هناك حاجة لذلك بعد التهيئة أعلاه)




# لتشغيل static على render
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



# ─── 2. تهيئة django-environ وقراءة .env ──────────────────────────────────────
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    USE_REMOTE_DB=(bool, False),
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# ─── 3. المفاتيح الأساسية والأمان ────────────────────────────────────────────
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Missing DJANGO_SECRET_KEY in environment")

DEBUG = os.getenv("DJANGO_DEBUG", "true").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    uri.strip()
    for uri in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if uri.strip()
]

# ─── 4. التطبيقات المثبتة ─────────────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "quiz",
    "accounts",

    "rest_framework",
    "corsheaders",
]

# ─── 5. الوسيطات (Middleware) ─────────────────────────────────────────────────
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
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



def get_env_or_raise(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value

USE_REMOTE_DB = os.getenv("USE_REMOTE_DB", "False").lower() in ("true", "1", "yes")

if USE_REMOTE_DB:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": get_env_or_raise("DB_NAME"),
            "USER": get_env_or_raise("DB_USER"),
            "PASSWORD": get_env_or_raise("DB_PASSWORD"),
            "HOST": get_env_or_raise("DB_HOST_EXTERNAL"),
            "PORT": os.getenv("DB_PORT", "5432"),
            "OPTIONS": {"sslmode": "require"},
        }
    }
else:
    DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     'quizdb',
        'USER':     'postgres',
        'PASSWORD': '123456',
        'HOST':     'localhost',
        'PORT':     '5432',
    }
}
# ─── 9. نموذج المستخدم المخصص ────────────────────────────────────────────────
AUTH_USER_MODEL = "accounts.CustomUser"

# ─── 10. التحقق من كلمات المرور ──────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
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

# ─── 13. إعدادات CORS ────────────────────────────────────────────────────────
# (تمت قراءتها أعلاه من env)
# CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])

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

# ─── 16. تسجيل الأخطاء على الكونسول (للمراقبة في Render) ────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "ERROR",
    },
}
