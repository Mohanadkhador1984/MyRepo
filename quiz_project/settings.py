# settings.py

from pathlib import Path

# ------------------------------------------------------------------------------
# 1. المسار الأساسي للمشروع
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------------------
# 2. الأمان
# ------------------------------------------------------------------------------
SECRET_KEY = 'your-very-unique-and-random-secret-key'  # غيّره في بيئة الإنتاج
DEBUG = True  # اجعله False في الإنتاج

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
    # تطبيقات Django الافتراضية
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # مكتبات الطرف الثالث
    'crispy_forms',
    'crispy_bootstrap4',
    'pwa',  # لدعم PWA تلقائيًا

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
    'whitenoise.middleware.WhiteNoiseMiddleware',  # لضغط وتقديم static في الإنتاج
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ------------------------------------------------------------------------------
# 5. الروتس و WSGI/ASGI
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'quiz_project.urls'
WSGI_APPLICATION = 'quiz_project.wsgi.application'
# if using ASGI:
# ASGI_APPLICATION = 'quiz_project.asgi.application'


# ------------------------------------------------------------------------------
# 6. القوالب (Templates)
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # قالب عام: base.html، errors.html…
        'APP_DIRS': True,  # يبحث تلقائيًا في كل app/templates/
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # auth & csrf
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ------------------------------------------------------------------------------
# 7. قاعدة البيانات (PostgreSQL)
# ------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------
# 8. Validators لكلمات المرور
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ------------------------------------------------------------------------------
# 9. التدويل والمنطقة الزمنية
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True


# ------------------------------------------------------------------------------
# 10. ملفات الستاتيك (Static Files)
# ------------------------------------------------------------------------------
# مسار URL لطلب static
STATIC_URL = '/staticfiles/'


# أثناء التطوير: Django يلتقط تلقائيًا:
#  - BASE_DIR/static/
#  - كل مجلد static/ داخل كل تطبيق
# لكن يمكنك إضافة أي مجلد إضافي هنا:
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # مجلد عام (pwa/, icons/, مشترك)
    # إن احتجت موارد مشتركة أخرى خارج هذا:
    # BASE_DIR / 'assets',
]

# عند تنفيذ collectstatic في الإنتاج:
STATIC_ROOT = BASE_DIR / 'staticfiles'

# لضغط وتجميع ملفات الستاتيك مع cache-busting
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ------------------------------------------------------------------------------
# 11. ملفات الميديا (User-uploaded Media)
# ------------------------------------------------------------------------------
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ------------------------------------------------------------------------------
# 12. تسجيل الدخول وإعادة التوجيه
# ------------------------------------------------------------------------------
LOGIN_REDIRECT_URL  = '/home/'
LOGIN_URL           = '/login/'
LOGOUT_REDIRECT_URL = '/login/'


# ------------------------------------------------------------------------------
# 13. إعدادات PWA
# ------------------------------------------------------------------------------
PWA_APP_NAME             = 'Quiz App'
PWA_APP_DESCRIPTION      = "تطبيق ويب دون اتصال"
PWA_APP_THEME_COLOR      = '#0A0302'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY          = 'standalone'
PWA_APP_SCOPE            = '/'
PWA_APP_START_URL        = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS            = [
    {
        'src': '/static/pwa/icons/icon-192x192.png',
        'sizes': '192x192',
    },
    {
        'src': '/static/pwa/icons/icon-512x512.png',
        'sizes': '512x512',
    },
]


# ------------------------------------------------------------------------------
# 14. تعريب لاحق (إن أردت)
# ------------------------------------------------------------------------------
# LANGUAGE_CODE = 'ar'
# LOCALE_PATHS = [BASE_DIR / 'locale']
