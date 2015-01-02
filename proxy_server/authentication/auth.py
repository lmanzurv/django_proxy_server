# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User as dUser
from django.core.cache import cache
from django.utils.translation import ugettext as _
from proxy_server.backend_services import invoke_backend_service
from proxy_server.helpers import generate_service_url
from novtory_admin import helpers
import base64, proxy_server

class ProxyServerBackend:
    supports_anonymous_user = False
    supports_inactive_user = False

    def _create_user(self, pk, user_dict):
        user = None
        if user_dict:
            username = user_dict['email']

            user = User(username=username)
            user.is_staff = False
            user.is_superuser = False
            user.is_active = user_dict['is_active']
            user.id = base64.b64encode(str(username))
            user.pk = pk
            user.backend = 'novtory_admin.auth.AuthBackend'
            user.first_name = user_dict['name']
            user.email = username

        return user

    def authenticate(self, username=None, password=None, request=None):
        try:
            # Invoke que web service that logs in
            url = generate_service_url('/login')
            data = dict(email=username, password=password, role='admin', platform='admin_web')
            status, response = invoke_backend_service('POST', url, json_data=data, public=True, request=request)
            if status == 200:
                # Create the logged user and set its attributes
                user = self._create_user(request.user.pk, response)
                cache.set(request.user.pk, user.to_dict())
                return user
            elif status == 204:
                raise Exception(_(u'El servicio web no retornó el usuario especificado'))
            elif status == 400 or status == 500:
                raise Exception(response[proxy_server.ERROR][proxy_server.MESSAGE].encode('utf8'))
            else:
                raise Exception(helpers._OPERATION_ERROR.encode('utf-8'))

        except Exception as e:
            raise Exception(str(e))

    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active:
            return False
        return user_obj.has_perm(perm, obj)

class User(dUser):

    def __init__(self, **kwargs):
        self.username = kwargs.pop('username', None)
        self.password = kwargs.pop('password', None)
        self.objects = None

    def save(self, **kwargs):
        pass

    def get_group_permissions(self):
        return list()

    def get_and_delete_messages(self):
        return list()

    def has_perm(self, perm, obj=None):
        return perm in self.roles

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
            email=self.email
        )

        return result
