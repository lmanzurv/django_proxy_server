from django.shortcuts import HttpResponse
from django.core.cache import cache

AJAX_REQUEST = 'ajax_request'
class ProxyHttpResponse(HttpResponse):
    def __init__(self, request, *args, **kwargs):
        super(ProxyHttpResponse, self).__init__( *args, **kwargs)
        cache.set(AJAX_REQUEST, request.user.pk)
