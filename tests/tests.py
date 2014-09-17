import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from django.test import TestCase
from proxy_server.backend_services import invoke_backend_service
from proxy_server.helpers import generate_service_url
from django.test.client import Client

class ProxyServicesTest(TestCase):
    def test_invoke_backend_service(self):
        c = Client(enforce_csrf_checks=True)

        response = c.get('/test_undecorated/')
        print 'Test undecorated view GET:', response.status_code

        response = c.post('/test_undecorated/')
        print 'Test undecorated view POST:', response.status_code, response.context['reason']

        response = c.post('/test/', **{'HTTP_API_KEY':'^ugfp@+cw!+se1b8kw%!23(sbrzk8f!uzrhqp$s)@67g9f1tdj', 'HTTP_X_FORWARDED_FOR':'127.0.0.1'})
        print 'Invoke backend as proxy response 200 cookies:', response.cookies
        print 'Invoke backend as proxy response 200 content:', response.content

        try:
            c.get('/test_error/', **{'HTTP_API_KEY':'^ugfp@+cw!+se1b8kw%!23(sbrzk8f!uzrhqp$s)@67g9f1tdj', 'HTTP_X_FORWARDED_FOR':'127.0.0.1'})
        except Exception as e:
            print 'Invoke backend as proxy response 500:', str(e)

        response = c.get('/test_token_validation/', **{'HTTP_API_KEY':'^ugfp@+cw!+se1b8kw%!23(sbrzk8f!uzrhqp$s)@67g9f1tdj', 'HTTP_X_FORWARDED_FOR':'127.0.0.1', 'HTTP_USER_TOKEN':'123token'})
        print 'Invoke backend as proxy response token_validation content:', response.content

class BackendServicesTest(TestCase):
    def test_invoke_backend_service(self):
        service_url = generate_service_url('/login')
        response = invoke_backend_service('POST', service_url, json_data={ 'email':'admin@test.com', 'password':'password' })
        print 'Invoke backend response 200: ', response

        try:
            invoke_backend_service('POST', service_url, json_data={ 'email':'admin@test.com' })
        except Exception as e:
            print 'Invoke backend response 500: ', str(e)
