SECRET_KEY = "FUCKIT"
from leselys.settings import *

ENV = "dev"
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'leselys.db'),
    }
}
SECRET_KEY = "f_!db_*)(1usnm8u9)q3goiuwrngg*r^h1kqd3l)p)9lxhyy4s"
INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    #'debug_toolbar.panels.profiling.ProfilingDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.cache.CacheDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
INTERNAL_IPS = ('127.0.0.1',)
TAG = 'body'

STATIC_ROOT = os.path.join(SITE_ROOT, "static")
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, "leselys", "assets"),
)

LOCALE_INDEPENDENT_PATHS = (
    r'^/static',
    r'^/media',
)

ALLOWED_HOSTS = ['localhost']
