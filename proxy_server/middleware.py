from django.core.urlresolvers import resolve

class DisableCSRF(object):
    def process_request(self, request):
        func, args, kwargs = resolve(request.path)
        if hasattr(func, '_proxy_service'):
            setattr(request, '_dont_enforce_csrf_checks', True)
