"""
Django settings for quiz_project (backend).

This configuration supports:
  - Local PostgreSQL DB (development)
  - Remote PostgreSQL DB on Render (production)
  - Serving a Vue PWA build (dist/) via WhiteNoise
  - CORS for Vue dev server and production domain
  - JWT authentication for the REST API
  - All secrets and flags driven by a single .env file
"""

import os
from pathlib import Path

import environ

# ─── 1. BASE DIRECTORIES ─────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
# Folder where Vue's production build (npm run build) outputs index.html, service-worker.js, etc.
DIST_DIR = BASE_DIR / "frontend_build" / "dist"

# ─── 2. LOAD ENVIRONMENT VARIABLES ───────────────────────────────────────────
# Initialize django-environ
env = environ.Env(
    # cast vars
    DJANGO_DEBUG=(bool, False),
    USE_REMOTE_DB=(bool, False),
)

# read .env file at BASE_DIR/.env
environ.Env.read_env(BASE_DIR / ".env")

# ─── 3. SECURITY & DEBUG ──────────────────────────────────────────────────────
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DJANGO_DEBUG")

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1"]
)

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=[]
)

# ─── 4. INSTALLED APPS ─────────────────────────────────────────────────────────
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Your apps
    "quiz",
    "accounts",

    # Third-party
    "rest_framework",
    "corsheaders",
]

# ─── 5. MIDDLEWARE ─────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",           # handle CORS
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",      # serve static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ─── 6. URLS & WSGI ───────────────────────────────────────────────────────────
ROOT_URLCONF = "quiz_project.urls"
WSGI_APPLICATION = "quiz_project.wsgi.application"

# ─── 7. TEMPLATES ─────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [DIST_DIR],  # serve Vue's index.html
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ─── 8. DATABASE CONFIGURATION ────────────────────────────────────────────────
# Flag to switch between local and remote DB
USE_REMOTE_DB = env.bool("USE_REMOTE_DB", default=False)

# ─── إعداد قاعدة البيانات ─────────────────────────────────────────────────
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

# ─── 9. AUTHENTICATION & VALIDATION ────────────────────────────────────────────
AUTH_USER_MODEL = "accounts.CustomUser"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─── 10. INTERNATIONALIZATION ──────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ─── 11. STATIC FILES & WHITENOISE ────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# include Vue build dir in static search
STATICFILES_DIRS = [DIST_DIR]

# serve root PWA files (service-worker.js, manifest.json, offline.html)
WHITENOISE_ROOT = str(DIST_DIR)

# long-term cache headers + versioned filenames
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ─── 12. CORS SETTINGS ────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=["http://localhost:8080"]
)

# ─── 13. DJANGO REST FRAMEWORK ────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}

# ─── 14. DEFAULT AUTO FIELD ───────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
