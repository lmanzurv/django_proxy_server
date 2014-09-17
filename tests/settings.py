DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'proxy_server.middleware.DisableCSRF',
)

SECRET_KEY = 'askjfadl#aksjdkasdl!aksjfkadfl)'

BACKEND_HOST = '0.0.0.0'
BACKEND_PORT = '8001'

ROOT_URLCONF = 'urls'

PROXY_API_KEYS = ['^ugfp@+cw!+se1b8kw%!23(sbrzk8f!uzrhqp$s)@67g9f1tdj', 'http://127.0.0.1:8001/']
PROXY_TOKEN_VALIDATION_SERVICE = 'tests.rest_api_connection.renew_session'
