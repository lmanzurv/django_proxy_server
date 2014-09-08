# -*- encoding: utf-8 -*-
from proxy_server.backend_services import invoke_backend_service_as_proxy
from proxy_server.helpers import generate_service_url

def renew_session(request):
    response = invoke_backend_service_as_proxy('POST', generate_service_url('/renew_session'), request=request, response_token=True)
    return response