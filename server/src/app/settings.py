import os
import environ


env = environ.Env(
    DEBUG = (bool, True)
)
environ.Env.read_env()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = env("SECRET_KEY", default='i_i-dw20qqpwbeq+f*3%ii%o(drnss5o=mkiezp_utyot4%3ls')

DEBUG = env("DEBUG")

AUTH_USER_MODEL = 'accounts.User'

ALLOWED_HOSTS = [
    'localhost',
    'budget-manager-backend.herokuapp.com',
    '127.0.0.1',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'currencies',
    'wallets',

    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_WHITELIST = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "https://budget-manager-client.herokuapp.com",
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.postgresql',
        'NAME' : 'budget-manager',
        'USER' : 'postgres',
        'PASSWORD' : 'Riopop123',
        'HOST' : 'localhost',
        'PORT' : '5432'
    } 
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_URL = '/static/'
STATIC_ROOT_PATH = env("STATIC_ROOT_PATH", cast=str, default="static_root")
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", STATIC_ROOT_PATH)

MEDIA_URL = '/media/'
MEDIA_ROOT_PATH = env("MEDIA_ROOT_PATH", cast=str, default="media_root")
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", MEDIA_ROOT_PATH)

# SSL/ TLS
if not DEBUG:
    CORS_REPLACE_HTTPS_REFERER      = True
    HOST_SCHEME                     = "https://"
    SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT             = True
    SESSION_COOKIE_SECURE           = True
    CSRF_COOKIE_SECURE              = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
    SECURE_HSTS_SECONDS             = 1000000
    SECURE_FRAME_DENY               = True
else:
    CORS_REPLACE_HTTPS_REFERER      = False
    HOST_SCHEME                     = "http://"
    SECURE_PROXY_SSL_HEADER         = None
    SECURE_SSL_REDIRECT             = False
    SESSION_COOKIE_SECURE           = False
    CSRF_COOKIE_SECURE              = False
    SECURE_HSTS_SECONDS             = None
    SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
    SECURE_FRAME_DENY               = False
