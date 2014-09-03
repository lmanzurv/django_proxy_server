class WsResponseError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def str(self):
        return 'WS response error: {0}'.format(repr(self.msg))

class WsInvocationError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def str(self):
        return 'WS invocation error: {0}'.format(repr(self.msg))