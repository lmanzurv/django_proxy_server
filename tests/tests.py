import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from django.test import TestCase
from proxy_server.backend_services import invoke_backend_service
from proxy_server.helpers import generate_service_url
from django.test.client import Client
import proxy_server

class ProxyServicesTest(TestCase):

    def test_invoke_backend_service(self):
        c = Client()
        response = c.get('/test')
        print 'View response:', response.status_code

class BackendServicesTest(TestCase):
    def test_invoke_backend_service(self):
        service_url = generate_service_url('/public/voter_location', params={ 'id_number':'0521220002', 'doc_type_code':'CU' }, encrypted=True)
        response = invoke_backend_service('GET', service_url)
        if response[proxy_server.MESSAGE] == proxy_server.SUCCESS:
            print 'Backend service success: ', response
        else:
            raise Exception(response[proxy_server.MESSAGE])