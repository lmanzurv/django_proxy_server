django_proxy_server
===================
This is a django application to use django as a proxy server between a frontend device/server and a backend server inside a militarized zone. Services are exposed using Django REST Framework. To identify itself, django-proxy-server uses the SECRET_KEY variable defined in settings as its API KEY.

Quick start
-----------
Install using pip or easy_install

    $ pip install django-proxy-server

    $ easy_install django-proxy-server

Add "proxy_server" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = ( 
        ...
        'proxy_server',
    )

Add the following options to the settings.py file to configure:

    PROXY_API_KEYS = [
        # Add the API KEYS you wish to allow consuming services
        # API KEYS are required. Services cannot be consumed without an API KEY
    ]
    
    # Write the route to the service you wish to use as token validation.
    # If you don't wish to have a token validation, skip this setting
    PROXY_TOKEN_VALIDATION_SERVICE = 'project.services.token_service'

    # The IP or domain address of the backend services to be consumed
    BACKEND_HOST = '127.0.0.1'

    # The port through which the backend services will be consumed
    BACKEND_PORT = '8000'

Usage
-----------
To expose a service using Django, simply decorate a view with
    
    # The option methods is a list of HTTP methods that can be exposed.
    # For example: GET, POST, PUT, DELETE
    # The option public indicates that the service will be exposed as public,
    # thus it doesn't require for the header to include a USER_TOKEN value
    @expose_service([ methods ], public=True)

There are two ways of invoking backend services, from a traditional Django view or from an external device that uses Django as a proxy server. The functions to invoke backend services relies on the helper function generate_service_url.

The function generate_service_url allows appending parameters to a URL, as well as encrypting them if the kwarg encrypted is set to True (by default, it is False).

When using traditional Django views, invoke services as follows:

    from proxy_server.backend_services import invoke_backend_service
    from proxy_server.helpers import generate_service_url

    def function(request):
        ...
        response = invoke_backend_service('GET', generate_service_url('/get_user', params={ 'username':'proxy_server_admin' }, encrypted=True))
        ...

The invoke_backend_service receives the following parameters:
* method: The method of the service to be invoked
* function_path: The path of the service URL
* json_data: A dictionary with the body content of the service. Default value: empty dict.
* request: The request of the Django view with the information of the user and headers
* response_token: Boolean argument that indicates if a response token is expected. By default, the service expects a token on response.
* public: Boolean argument that indicates if the accessed service is public. By default, the invoked services are not public.

When using Django as a proxy server, invoke services as follows:

    from proxy_server.decorators import expose_service
    from proxy_server.helpers import generate_service_url
    from proxy_server.backend_services import invoke_backend_service_as_proxy
    import proxy_server

    @expose_service(['GET'])
    def home(request):
        ...
        response = invoke_backend_service_as_proxy('GET', generate_service_url('/get_user', params={ 'username':'proxy_server_admin' }, encrypted=True))
        ...

The invoke_backend_service_as_proxy receives the following parameters:
* method: The method of the service to be invoked
* function_path: The path of the service URL
* json_data: A dictionary with the body content of the service. Default value: empty dict.
* request: The request of the Django view with the information of the user and headers
* response_token: Boolean argument that indicates if a response token is expected. By default, the service expects a token on response.
