from django.contrib.auth import SESSION_KEY
from django.conf import settings
from errors import WsResponseError, WsInvocationError
import httplib, json, proxy_server

def invoke_backend_service(method, function_path, json_data=dict(), request=None, response_token=True, public=False, secure=False):
    if hasattr(settings, 'BACKEND_HOST'):
        if secure:
            if hasattr(settings, 'BACKEND_PORT'):
                conn = httplib.HTTPSConnection(settings.BACKEND_HOST, settings.BACKEND_PORT)
            else:
                conn = httplib.HTTPSConnection(settings.BACKEND_HOST)
        else:
            if hasattr(settings, 'BACKEND_PORT'):
                conn = httplib.HTTPConnection(settings.BACKEND_HOST, settings.BACKEND_PORT)
            else:
                raise WsInvocationError('No port supplied')
            
        if request is not None:
            headers = proxy_server.RESTFUL_HEADER
            headers[proxy_server.USER_TOKEN] = request.user.pk
            headers[proxy_server.CLIENT_IP] = request.META.get(proxy_server.HTTP_FROM)
            headers[proxy_server.API_KEY] = settings.SECRET_KEY

            conn.request(method, function_path, json.dumps(json_data), headers)
        else:
            conn.request(method, function_path, json.dumps(json_data), proxy_server.RESTFUL_HEADER)
        
        response = conn.getresponse()
        
        if response.status is 200:
            response_data = response.read()
            conn.close()
            
            response = json.loads(response_data)

            if not public and not response_token:
                if response_token and proxy_server.USER_TOKEN not in response:
                    raise WsResponseError(response[proxy_server.RESPONSE_MESSAGE])
                
                if proxy_server.USER_TOKEN in response and request is not None:
                    request.session[SESSION_KEY] = response[proxy_server.USER_TOKEN]
                    request.user.pk = response[proxy_server.USER_TOKEN]
                    del response[proxy_server.USER_TOKEN]

            elif public and response_token:
                raise WsInvocationError('A web service cannot be public and expect a response token')
            
            return response
        else:
            conn.close()
            raise WsResponseError(response.reason)
    else:
        raise WsInvocationError('No backend host and/or port specified')

def invoke_backend_service_as_proxy(method, function_path, json_data=dict(), request=None, response_token=False, secure=False):
    if hasattr(settings, 'BACKEND_HOST'):
        if secure:
            if hasattr(settings, 'BACKEND_PORT'):
                conn = httplib.HTTPSConnection(settings.BACKEND_HOST, settings.BACKEND_PORT)
            else:
                conn = httplib.HTTPSConnection(settings.BACKEND_HOST)
        else:
            if hasattr(settings, 'BACKEND_PORT'):
                conn = httplib.HTTPConnection(settings.BACKEND_HOST, settings.BACKEND_PORT)
            else:
                raise WsInvocationError('No port supplied')

        if request is not None:
            headers = proxy_server.RESTFUL_HEADER
            headers[proxy_server.USER_TOKEN] = request.META.get(proxy_server.HTTP_USER_TOKEN)
            headers[proxy_server.CLIENT_IP] = request.META.get(proxy_server.HTTP_FROM)
            headers[proxy_server.API_KEY] = request.META.get(proxy_server.HTTP_API_KEY)
            try:
                conn.request(method, function_path, json.dumps(json_data), headers)
            except:
                raise WsInvocationError('Could not connect to service')
        else:
            conn.request(method, function_path, json.dumps(json_data), proxy_server.RESTFUL_HEADER)

        response = conn.getresponse()

        if response.status is 200:
            response_data = response.read()
            conn.close()
            response = json.loads(response_data)
            if response_token and proxy_server.USER_TOKEN not in response:
                raise WsResponseError(response[proxy_server.RESPONSE_MESSAGE])
            
            return response
        else:
            conn.close()
            raise WsResponseError(response.reason)
    else:
        raise WsInvocationError('No backend host and/or port specified')