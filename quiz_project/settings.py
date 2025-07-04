import os
from pathlib import Path
from dotenv import load_dotenv

# ------------------------------------------------------------------------------
# 1) تحميل المتغيرات من .env
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# ------------------------------------------------------------------------------
# 2) مفاتيح الأمان و DEBUG
# ------------------------------------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

# ------------------------------------------------------------------------------
# 3) Hosts و CSRF
# ------------------------------------------------------------------------------
# 1) تفعيل أو تعطيل وضع التصحيح عبر متغير بيئي DJANGO_DEBUG
#    القيم المقبولة: "True", "true", "1", "yes" لتفعيل الـ Debug
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in ("true", "1", "yes")

# 2) بناء القيمة الافتراضية لقائمة المضيفين المسموح بها حسب وضع الـ Debug
if DEBUG:
    default_hosts = "localhost,127.0.0.1"
else:
    default_hosts = "myrepo-28.onrender.com"

# 3) قراءة المتغير أو استخدام الافتراضي
raw_hosts = os.getenv("ALLOWED_HOSTS", default_hosts)
ALLOWED_HOSTS = [h.strip() for h in raw_hosts.split(",") if h.strip()]

# 4) (اختياري) طباعة القيم محلياً للتأكد
if DEBUG:
    print("DEBUG =", DEBUG)
    print("ALLOWED_HOSTS =", ALLOWED_HOSTS)

    
# 2) قراء CSRF_TRUSTED_ORIGINS وتحويل كل قيمة إلى عنوان صحيح
raw_csrf = os.getenv("CSRF_TRUSTED_ORIGINS", raw_hosts)
CSRF_TRUSTED_ORIGINS = []
for origin in raw_csrf.split(","):
    o = origin.strip()
    if not o:
        continue
    # إذا لم يبدأ بـ http:// أو https:// نضيف https://
    if not o.startswith(("http://", "https://")):
        o = f"https://{o}"
    CSRF_TRUSTED_ORIGINS.append(o)


# ------------------------------------------------------------------------------
# 4) قواعد البيانات (محلي / بعيد)
# ------------------------------------------------------------------------------
USE_REMOTE_DB = os.getenv("USE_REMOTE_DB", "False").lower() in ("true", "1", "yes")

if USE_REMOTE_DB:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST_EXTERNAL"),
            "PORT": os.getenv("DB_PORT", "5432"),
            "OPTIONS": {"sslmode": "require"},
        }
    }
else:
    local_engine = os.getenv("DATABASE_LOCAL_ENGINE", "sqlite3")
    if local_engine == "sqlite3":
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / os.getenv("DATABASE_LOCAL_NAME", "db.sqlite3"),
            }
        }
    else:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": os.getenv("DATABASE_LOCAL_NAME"),
                "USER": os.getenv("DATABASE_LOCAL_USER"),
                "PASSWORD": os.getenv("DATABASE_LOCAL_PASSWORD"),
                "HOST": os.getenv("DATABASE_LOCAL_HOST"),
                "PORT": os.getenv("DATABASE_LOCAL_PORT", "5432"),
            }
        }

# ------------------------------------------------------------------------------
# 5) التطبيقات والوسيطات وقوالب العرض
# ------------------------------------------------------------------------------
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

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# ------------------------------------------------------------------------------
# 6) المصادقة والمسارات الثابتة والوسائط
# ---------------------------------------A---------------------------------------

CRISPY_TEMPLATE_PACK = "bootstrap4"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_REDIRECT_URL = "/home/"
LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "/login/"

# ------------------------------------------------------------------------------
# 7) إعدادات PWA
# ------------------------------------------------------------------------------
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
