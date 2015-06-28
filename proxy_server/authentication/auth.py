# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User as DjangoUser
from django.core.cache import cache
from proxy_server.backend_services import invoke_backend_service
from proxy_server.helpers import generate_service_url
import base64, proxy_server

class ProxyServerBackend:
    supports_anonymous_user = False
    supports_inactive_user = False

    def _create_user(self, pk, user_dict):
        user = None
        if user_dict:
            username = user_dict.pop('email')

            user = User(username=username)
            user.is_staff = False
            user.is_superuser = False
            user.is_active = user_dict.pop('is_active')
            user.id = base64.b64encode(str(username))
            user.pk = pk
            user.backend = 'proxy_server.authentication.auth.ProxyServerBackend'
            user.first_name = user_dict.pop('name')
            user.email = username

            for key, value in user_dict.iteritems():
                setattr(user, key, value)

        return user

    def authenticate(self, username=None, password=None, **kwargs):
        request = kwargs.pop('request', None)

        if not request:
            raise Exception('Django\'s request is required to authenticate')

        try:
            # Invoke que web service that logs in
            url = generate_service_url('/login')
            data = dict(email=username, password=password)
            data.update(kwargs)

            status, response = invoke_backend_service('POST', url, json_data=data, public=True, request=request)
            if status == 200:
                # Create the logged user and set its attributes
                user = self._create_user(request.user.pk, response)
                cache.set(request.user.pk, user.to_dict())
                return user
            elif status == 204:
                raise Exception('Web service did not return a valid user')
            elif status == 400 or status == 500:
                raise Exception(response[proxy_server.ERROR][proxy_server.MESSAGE].encode('utf8'))
            else:
                raise Exception('Authentication error')

        except Exception as e:
            raise Exception(str(e))

    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active:
            return False
        return user_obj.has_perm(perm, obj)

class User(DjangoUser):

    def __init__(self, **kwargs):
        self.username = kwargs.pop('username', None)
        self.password = kwargs.pop('password', None)
        self.objects = None
        self.permissions = list()

    def save(self, **kwargs):
        changed = False
        for name, value in kwargs.iteritems():
            if name is not 'pk':
                changed = True

                if name is 'name':
                    setattr(self, 'first_name', value)
                else:
                    setattr(self, name, value)

        if changed:
            cache.set(self.pk, self.to_dict())

    def get_group_permissions(self):
        return list()

    def get_and_delete_messages(self):
        return list()

    def has_perm(self, perm, obj=None):
        return perm in self.permissions

    def has_perms(self, perm_list, obj=None):
        for perm in perm_list:
            if self.has_perm(perm):
                return True
        return False

    def to_dict(self):
        result = dict(
            username=self.username,
            is_staff=self.is_staff,
            is_superuser=self.is_superuser,
            is_active=self.is_active,
            id=self.id,
            pk=self.pk,
            backend=self.backend,
            name=self.first_name,
            email=self.email,
            permissions=self.permissions
        )

        attrs = [attr for attr in self.__dict__.keys() if not attr.startswith('__') and not attr.endswith('__')]
        for attr in attrs:
            result.update({ attr: getattr(self, attr) })

        return result
