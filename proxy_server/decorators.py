from functools import wraps
from rest_framework.decorators import api_view
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseServerError
from django.conf import settings
from importlib import import_module
import proxy_server

def expose_service(methods):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if hasattr(settings, 'PROXY_API_KEYS'):
                if request.META.get(proxy_server.HTTP_API_KEY) in settings.PROXY_API_KEYS:
                    if hasattr(settings, 'PROXY_TOKEN_VALIDATION_SERVICE'):
                        if request.META.get(proxy_server.HTTP_USER_TOKEN):

                            try:
                                dot = settings.PROXY_TOKEN_VALIDATION_SERVICE.rindex('.')
                            except ValueError:
                                return HttpResponseServerError('Token validation service not properly configured')
                            
                            val_module = import_module(settings.PROXY_TOKEN_VALIDATION_SERVICE[:dot])
                            val_func = getattr(val_module, settings.PROXY_TOKEN_VALIDATION_SERVICE[dot + 1:])

                            response = val_func(request)
                            if response[proxy_server.MESSAGE] == proxy_server.SUCCESS:
                                request.META[proxy_server.HTTP_USER_TOKEN] = response[proxy_server.USER_TOKEN]
                                return api_view(methods)(view_func)(request, *args, **kwargs)
                    else:
                        return api_view(methods)(view_func)(request, *args, **kwargs)
            raise PermissionDenied
        return wraps(view_func)(wrapper)
    return decorator