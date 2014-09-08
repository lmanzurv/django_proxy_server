from django.http import HttpResponse
from proxy_server.decorators import expose_service
from proxy_server.backend_services import invoke_backend_service_as_proxy
from proxy_server.helpers import generate_service_url
import json

@expose_service(['GET'], public=True)
def test(request):
    service_url = generate_service_url('/login')
    response = invoke_backend_service_as_proxy('POST', service_url, json_data={ 'email':'admin@test.com', 'password':'password' }, request=request)
    return HttpResponse(json.dumps(response), content_type='application/json')

@expose_service(['GET'], public=True)
def test_error(request):
    service_url = generate_service_url('/login')
    response = invoke_backend_service_as_proxy('POST', service_url, json_data={ 'email':'admin@test.com' }, request=request)
    return HttpResponse(json.dumps(response), content_type='application/json')

@expose_service(['GET'])
def test_token_validation(request):
    service_url = generate_service_url('/login')
    response = invoke_backend_service_as_proxy('POST', service_url, json_data={ 'email':'admin@test.com', 'password':'password' }, request=request)
    return HttpResponse(json.dumps(response), content_type='application/json')