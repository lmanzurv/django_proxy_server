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
            
        headers = proxy_server.RESTFUL_HEADER

        if request is not None:
            
            headers[proxy_server.USER_TOKEN] = request.user.pk
            headers[proxy_server.CLIENT_IP] = request.META.get(proxy_server.HTTP_FROM)
            headers[proxy_server.API_KEY] = settings.SECRET_KEY

        try:
            conn.request(method, function_path, json.dumps(json_data), headers)
        except:
            raise WsInvocationError('Could not connect to service')
        
        response = conn.getresponse()
        response_data = response.read()
        conn.close()
        
        response_json = json.loads(response_data)

        if response.status is 200:
            if public == True and response_token == True:
                raise WsInvocationError('A web service cannot be public and expect a response token')
            
            elif public == False and response_token == True:
                if proxy_server.USER_TOKEN not in response_json:
                    raise WsResponseError('Server expected user token in response')
                
                if proxy_server.USER_TOKEN in response_json:
                    if request is not None:
                        request.session[SESSION_KEY] = response_json[proxy_server.USER_TOKEN]
                        request.user.pk = response_json[proxy_server.USER_TOKEN]
                        request.session[proxy_server.EXPIRATION_DATE] = response_json[proxy_server.EXPIRATION_DATE]
            
            return response_json[proxy_server.RESPONSE]
        else:
            if proxy_server.ERROR in response_json:
                raise WsResponseError(response_json[proxy_server.ERROR][proxy_server.MESSAGE])
            else:
                raise WsResponseError('Unknown error in backend server')
    else:
        raise WsInvocationError('No backend host and/or port specified')

def invoke_backend_service_as_proxy(method, function_path, json_data=dict(), request=None, response_token=True, secure=False):
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

        headers = proxy_server.RESTFUL_HEADER

        if request is not None:
            headers[proxy_server.USER_TOKEN] = request.META.get(proxy_server.HTTP_USER_TOKEN)
            headers[proxy_server.CLIENT_IP] = request.META.get(proxy_server.HTTP_FROM)
            headers[proxy_server.API_KEY] = request.META.get(proxy_server.HTTP_API_KEY)

        try:
            conn.request(method, function_path, json.dumps(json_data), headers)
        except:
            raise WsInvocationError('Could not connect to service')

        response = conn.getresponse()
        response_data = response.read()
        conn.close()

        response_json = json.loads(response_data)

        if response.status is 200:
            if response_token and proxy_server.USER_TOKEN not in response_json:
                raise WsResponseError('Server expected user token in response')
            
            return response_json
        else:
            if proxy_server.ERROR in response_json:
                raise WsResponseError(response_json[proxy_server.ERROR][proxy_server.MESSAGE])
            else:
                raise WsResponseError('Unknown error in backend server')
    else:
        raise WsInvocationError('No backend host and/or port specified')