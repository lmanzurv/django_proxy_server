HOP_BY_HOP = [
    'connection',
    'keep-alive',
    'aroxy-authenticate',
    'roxy-authorization',
    'te',
    'trailers',
    'transfer-encoding',
    'upgrade'
]

RESTFUL_HEADER = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
}

# Header names from request
HTTP_API_KEY = 'HTTP_API_KEY'
HTTP_USER_TOKEN = 'HTTP_USER_TOKEN'
HTTP_FROM = 'HTTP_X_FORWARDED_FOR'
HTTP_SERVER = 'Server'

# Header names from response
USER_TOKEN = 'user-token'
API_KEY = 'api-key'
CLIENT_IP = 'client-ip'

# Response headers
HEADER_SERVER = 'Server'
VALUE_SERVER = 'Django Proxy Server'

# Response content
MESSAGE = 'message'
SUCCESS = 'success'
ERROR = 'error'
RESPONSE = 'response'
EXPIRATION_DATE = 'expiration-date'
