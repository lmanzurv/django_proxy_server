from django.contrib.auth import SESSION_KEY
from django.core.cache import cache
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from proxy_server.response import AJAX_REQUEST
import httplib, json, proxy_server

def invoke_backend_service(method, function_path, json_data=dict(), request=None, response_token=True, public=False, secure=False):
    error_message = None

    try:
        if public is False and request is None:
            error_message = 'A private web service must receive Django\'s request'
            raise Exception

        if response_token is True and request is None:
            error_message = 'A web service cannot expect a response token and not receive Django\'s request'
            raise Exception

        if not hasattr(settings, 'BACKEND_HOST'):
            error_message = 'No backend host and/or port specified'
            raise Exception

        if secure:
            if hasattr(settings, 'BACKEND_PORT'):
                conn = httplib.HTTPSConnection(settings.BACKEND_HOST, settings.BACKEND_PORT)
            else:
                conn = httplib.HTTPSConnection(settings.BACKEND_HOST)
        else:
            if hasattr(settings, 'BACKEND_PORT'):
                conn = httplib.HTTPConnection(settings.BACKEND_HOST, settings.BACKEND_PORT)
            else:
                conn = httplib.HTTPConnection(settings.BACKEND_HOST)

        headers = proxy_server.RESTFUL_HEADER
        headers[proxy_server.API_KEY] = settings.SECRET_KEY

        if request is not None:
            pk = cache.get(AJAX_REQUEST, None)
            if pk:
                request.user.pk = pk
                cache.delete(AJAX_REQUEST)

            headers[proxy_server.USER_TOKEN] = request.user.pk
            headers[proxy_server.CLIENT_IP] = request.META.get(proxy_server.HTTP_FROM)

        try:
            conn.request(method, function_path, json.dumps(json_data), headers)
        except:
            error_message = 'Could not connect to service'
            raise Exception

        response = conn.getresponse()
        response_data = response.read()
        conn.close()

        if response.status == 403:
            return 403, None

        if response.status == 204:
            if response_token is True:
                error_message = 'Backend server didn\'t respond with a token'
                raise Exception

            return 204, None

        else:
            try:
                response_json = json.loads(response_data)
            except:
                error_message = 'Unknown response format'
                raise Exception

            if response_token is True:
                user_dict = None
                if SESSION_KEY in request.session:
                    user_dict = cache.get(request.session[SESSION_KEY])
                    cache.delete(request.session[SESSION_KEY])

                request.session[SESSION_KEY] = response_json[proxy_server.USER_TOKEN]
                request.user.pk = response_json[proxy_server.USER_TOKEN]
                request.session[proxy_server.EXPIRATION_DATE] = response_json[proxy_server.EXPIRATION_DATE]

                if user_dict:
                    user_dict['pk'] = request.user.pk
                    cache.set(request.session[SESSION_KEY], user_dict)

            if response.status == 200:
                if response_token is True and proxy_server.USER_TOKEN not in response_json:
                    error_message = 'Server expected user token in response'
                    raise Exception

                result = None
                if proxy_server.RESPONSE in response_json:
                    result = response_json[proxy_server.RESPONSE]

                return 200, result

            else:
                code = response.status

                if proxy_server.ERROR in response_json:
                    error_message = response_json[proxy_server.ERROR][proxy_server.MESSAGE]
                    raise Exception(code)
                else:
                    error_message = response.reason
                    raise Exception(code)

    except Exception as e:
        if error_message is None:
            error_message = 'Unknown error in service invocation'

        code = int(str(e)) if e is not None and isinstance(str(e), int) else 500
        error = {
            'error': {
                'code': code,
                'type': 'ProxyServerError',
                'message': error_message
            }
        }

        return code, error

def invoke_backend_service_as_proxy(request, method, function_path, json_data=dict(), response_token=True, secure=False):
    error_message = None

    try:
        if not hasattr(settings, 'BACKEND_HOST'):
            error_message = 'No backend host and/or port specified'
            raise Exception

        if secure:
            if hasattr(settings, 'BACKEND_PORT'):
                conn = httplib.HTTPSConnection(settings.BACKEND_HOST, settings.BACKEND_PORT)
            else:
                conn = httplib.HTTPSConnection(settings.BACKEND_HOST)
        else:
            if hasattr(settings, 'BACKEND_PORT'):
                conn = httplib.HTTPConnection(settings.BACKEND_HOST, settings.BACKEND_PORT)
            else:
                conn = httplib.HTTPConnection(settings.BACKEND_HOST)

        headers = proxy_server.RESTFUL_HEADER
        headers[proxy_server.USER_TOKEN] = request.META.get(proxy_server.HTTP_USER_TOKEN)
        headers[proxy_server.CLIENT_IP] = request.META.get(proxy_server.HTTP_FROM)
        headers[proxy_server.API_KEY] = request.META.get(proxy_server.HTTP_API_KEY)

        try:
            conn.request(method, function_path, json.dumps(json_data), headers)
        except:
            error_message = 'Could not connect to service'
            raise Exception

        response = conn.getresponse()
        response_data = response.read()
        conn.close()

        if response.status == 403:
            resp = HttpResponse(status=response.status, reason=response.reason)
            for header, value in response.getheaders():
                resp[header] = value

            for header in proxy_server.HOP_BY_HOP:
                del resp[header]

            resp[proxy_server.HEADER_SERVER] = proxy_server.VALUE_SERVER

            return resp

        if response.status == 204:
            if response_token is True:
                error_message = 'Backend server didn\'t respond with a token'
                raise Exception

            resp = HttpResponse(status=response.status, content_type='application/json', reason=response.reason)
            for header, value in response.getheaders():
                resp[header] = value

            for header in proxy_server.HOP_BY_HOP:
                del resp[header]

            resp[proxy_server.HEADER_SERVER] = proxy_server.VALUE_SERVER

            return resp
        else:
            try:
                response_json = json.loads(response_data)
            except:
                error_message = 'Unknown response format'
                raise Exception

            if response.status == 200:
                if response_token is True and proxy_server.USER_TOKEN not in response_json:
                    error_message = 'Server expected user token in response'
                    raise Exception

            resp = HttpResponse(response_data, status=response.status, content_type='application/json', reason=response.reason)
            for header, value in response.getheaders():
                resp[header] = value

            for header in proxy_server.HOP_BY_HOP:
                del resp[header]

            resp[proxy_server.HEADER_SERVER] = proxy_server.VALUE_SERVER

            return resp

    except Exception as e:
        if error_message is None:
            error_message = 'Unknown error in service invocation'

        code = int(str(e)) if e is not None and isinstance(str(e), int) else 500
        error = {
            'error': {
                'code': code,
                'type': 'ProxyServerError',
                'message': error_message
            }
        }

        return HttpResponseServerError(json.dumps(error), content_type='application/json')
