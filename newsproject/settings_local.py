DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kompoblog',
        'USER': 'newuser',
        'PASSWORD': 'user_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

from .settings import DEBUG
if DEBUG:
    from .settings import INSTALLED_APPS, MIDDLEWARE
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INSTALLED_APPS += (
        'debug_toolbar',
    )

    INTERNAL_IPS = ('127.0.0.1',)

    DEBUG_TOOLBAR_PANELS_ = [
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.cache.CacheDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    ]

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'ENABLE_STACKTRACES': True,
    }
