import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '=f^2e4hm1g(r^s37=ndk-__z^4c19!r43g%@rbh#=b5-2-j59o'

DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_LOADERS = ('django.template.loaders.app_directories.Loader', )

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'ckeditor',
    'autoslug',
    'taggit',
    'tagging',
    'postapp',
    'uni_paginator',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'newsproject.urls'

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

WSGI_APPLICATION = 'newsproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/home/pascal65536/git/my.cnf',
        },
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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Krasnoyarsk'

USE_I18N = True

USE_L10N = True

USE_TZ = True

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CKEDITOR_CONFIGS = {
    'default': {
        'allowedContent': True,
        'toolbar': [
            ['RemoveFormat', 'Undo', 'Redo', 'Source',
             '-', 'Bold', 'Italic', 'Underline',
             '-', 'Link', 'Unlink', 'Anchor',
             'Format'
             '-', 'Maximize',
             '-', 'Table',
             '-', 'Image',
             '-', 'NumberedList', 'BulletedList'
             ],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
             '-', 'Font', 'FontSize', 'TextColor',
             '-', 'Outdent', 'Indent',
             '-', 'HorizontalRule',
             '-', 'Blockquote'
             ]
        ],
    },
}
