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

SECRET_KEY = 'askjfadl#aksjdkasdl!aksjfkadfl)'

BACKEND_HOST = '0.0.0.0'
BACKEND_PORT = '8001'

ROOT_URLCONF = 'urls'

API_KEYS = ['^ugfp@+cw!+se1b8kw%!23(sbrzk8f!uzrhqp$s)@67g9f1tdj', 'http://127.0.0.1:8001/']
TOKEN_VALIDATION_SERVICE = 'novtory_frontend.rest_api_connection.renew_session'