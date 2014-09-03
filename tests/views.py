from django.http import HttpResponse
from proxy_server.decorators import expose_service

@expose_service(['GET'])
def test(request):
    print 'este es el view de test'
    return HttpResponse('The test view has been invoked')