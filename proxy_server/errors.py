class WsResponseError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'WS response error: {0}'.format(repr(self.message))

class WsInvocationError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

    def __str__(self):
        return 'WS invocation error: {0}'.format(repr(self.message))