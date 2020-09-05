import json

class getCookies(object):

    def __init__(self, request):
        self.request = request

    def __call__(self, name):
        cookies = json.loads(str(self.request.COOKIES).replace("\'", "\""))
        if name in cookies:
            return cookies[name]
        return None
            