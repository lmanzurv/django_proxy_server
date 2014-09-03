import base64

def generate_service_url(function_path, params=None, encrypted=False):
    if not params:
        return function_path
    else:
        path_end = str()
        for key, value in params.iteritems():
            if encrypted:
                value = base64.urlsafe_b64encode(str(value)).replace('=','')
            else:
                value = str(value)

            if not path_end:
                path_end += '?{0}={1}'.format(key, value)
            else:
                path_end += '&{0}={1}'.format(key, value)
        return function_path + path_end