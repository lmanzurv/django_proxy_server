from django.contrib.auth.signals import user_logged_out
from django.core.cache import cache

def logout(sender, request, user, **kwargs):
    cache.delete(request.user.pk)

user_logged_out.connect(logout)
