# -*- encoding: utf-8 -*-
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.conf import settings

class ProxyServerMiddleware(object):
    def process_request(self, request):
        if not hasattr(request, '_cached_user'):
            try:
                user_id = request.session[SESSION_KEY]
                backend_path = request.session[BACKEND_SESSION_KEY]
                assert backend_path in settings.AUTHENTICATION_BACKENDS
                backend = load_backend(backend_path)
                user_dict = cache.get(user_id)
                user = backend._create_user(user_id, user_dict) or AnonymousUser()
            except:
                user = AnonymousUser()

            request._cached_user = user

        request.user = request._cached_user
