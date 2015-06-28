from functools import wraps
from django.http import HttpResponse
from django.conf import settings
from importlib import import_module
import proxy_server, json

def expose_service(methods, public=False):
    def decorator(view_func):
        view_func.__dict__['_proxy_service'] = True

        def wrapper(request, *args, **kwargs):
            error_message = None
            code = 500

            try:
                if hasattr(settings, 'PROXY_API_KEYS'):
                    if request.META.get(proxy_server.HTTP_API_KEY) in settings.PROXY_API_KEYS:
                        rest_framework = False
                        if hasattr(settings, 'REST_FRAMEWORK_SUPPORT'):
                            rest_framework = settings.REST_FRAMEWORK_SUPPORT

                        if hasattr(settings, 'PROXY_TOKEN_VALIDATION_SERVICE'):
                            if public is True:
                                if request.META.get(proxy_server.HTTP_USER_TOKEN) is not None:
                                    error_message = 'A public service cannot receive a user token'
                                    code = 400
                                    raise Exception
                                else:
                                    if rest_framework:
                                        from rest_framework.decorators import api_view
                                        return api_view(methods)(view_func)(request, *args, **kwargs)
                                    else:
                                        if request.method not in methods:
                                            code = 405
                                            error_message = 'Method Not Allowed'
                                            raise Exception

                                        setattr(request, 'DATA', dict())
                                        if request.body:
                                            request.DATA.update(json.loads(request.body))

                                        return view_func(request, *args, **kwargs)
                            else:
                                if not request.META.get(proxy_server.HTTP_USER_TOKEN):
                                    error_message = 'A private service requires a user token'
                                    code = 400
                                    raise Exception
                                else:
                                    try:
                                        dot = settings.PROXY_TOKEN_VALIDATION_SERVICE.rindex('.')
                                    except ValueError:
                                        error_message = 'Token validation service not properly configured'
                                        raise Exception

                                    val_module = import_module(settings.PROXY_TOKEN_VALIDATION_SERVICE[:dot])
                                    val_func = getattr(val_module, settings.PROXY_TOKEN_VALIDATION_SERVICE[dot + 1:])

                                    try:
                                        response = val_func(request)
                                    except Exception as e:
                                        error_message = 'Could not invoke token validation service'
                                        raise Exception

                                    if response.status_code == 403:
                                        code = 403
                                        error_message = 'Token invalid'
                                        raise Exception

                                    response_json = json.loads(response.content)
                                    request.META[proxy_server.HTTP_USER_TOKEN] = response_json[proxy_server.USER_TOKEN]

                        if rest_framework:
                            from rest_framework.decorators import api_view
                            return api_view(methods)(view_func)(request, *args, **kwargs)
                        else:
                            if request.method not in methods:
                                code = 405
                                error_message = 'Method Not Allowed'
                                raise Exception

                            setattr(request, 'DATA', dict())
                            if request.body:
                                request.DATA.update(json.loads(request.body))

                            return view_func(request, *args, **kwargs)

                    else:
                        error_message = 'Received API KEY not found in server API KEYS set'
                        code = 403
                        raise Exception

                else:
                    error_message = 'API KEYS not properly configured'
                    raise Exception

            except Exception as e:
                if error_message is None:
                    if e.message is not None:
                        error_message = e.message

                    else:
                        error_message = 'Server encountered an error and cannot proceed with service call'

                error = {
                    'error': {
                        'code': code,
                        'type': 'ProxyServerError',
                        'message': error_message
                    }
                }

                return HttpResponse(json.dumps(error), content_type='application/json', status=code, reason=error_message)

        return wraps(view_func)(wrapper)
    return decorator
