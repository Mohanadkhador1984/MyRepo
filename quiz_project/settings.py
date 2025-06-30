from pathlib import Path
import os

# ------------------------------------------------------------------------------
# 1. المسار الأساسي للمشروع
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------------------
# 2. الأمان
# ------------------------------------------------------------------------------
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-dev-secret-key')  # استخدم متغير بيئة في الإنتاج
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'myrepo-28.onrender.com',
]

CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'https://myrepo-28.onrender.com',
]


# ------------------------------------------------------------------------------
# 3. التطبيقات المثبتة
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',

    # طرف ثالث
    'crispy_forms',
    'crispy_bootstrap4',
    'pwa',

    # تطبيقات المشروع
    'quiz',
    'account',
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# ------------------------------------------------------------------------------
# 4. الميدلوير
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # تقديم static files بكفاءة
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ------------------------------------------------------------------------------
# 5. الروت و WSGI
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'quiz_project.urls'
WSGI_APPLICATION = 'quiz_project.wsgi.application'


# ------------------------------------------------------------------------------
# 6. القوالب
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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


# ------------------------------------------------------------------------------
# 7. قاعدة البيانات
# ------------------------------------------------------------------------------
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}




# ------------------------------------------------------------------------------
# 8. التحقق من كلمات المرور
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ------------------------------------------------------------------------------
# 9. التدويل
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True


# static settings
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'  # مهم عند استخدام collectstatic للإنتاج

# PWA manifest and service worker
PWA_APP_NAME = 'Quiz App'
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static', 'pwa', 'serviceworker.js')


# ------------------------------------------------------------------------------
# 11. ملفات الميديا (التي يرفعها المستخدمون)
# ------------------------------------------------------------------------------
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ------------------------------------------------------------------------------
# 12. تسجيل الدخول
# ------------------------------------------------------------------------------
LOGIN_REDIRECT_URL  = '/home/'
LOGIN_URL           = '/login/'
LOGOUT_REDIRECT_URL = '/login/'


# ------------------------------------------------------------------------------
# 13. إعدادات PWA
# ------------------------------------------------------------------------------
PWA_APP_NAME             = 'Quiz App'
PWA_APP_DESCRIPTION      = "تطبيق يعمل دون اتصال"
PWA_APP_THEME_COLOR      = '#0A0302'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY          = 'standalone'
PWA_APP_SCOPE            = '/'
PWA_APP_START_URL        = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'

# استخدم {% static %} دائمًا للحصول على المسار الصحيح للصور
PWA_APP_ICONS = [
    {
  
  "icons":[
    {
      "src": "/static/pwa/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/pwa/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}

]

PWA_SERVICE_WORKER_PATH = BASE_DIR / 'static' / 'pwa' / 'service-worker.js'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ------------------------------------------------------------------------------
# 14. تعريب لاحق (اختياري)
# ------------------------------------------------------------------------------
# LANGUAGE_CODE = 'ar'
# LOCALE_PATHS = [BASE_DIR / 'locale']