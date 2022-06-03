from framework.request import Request
from framework.responses import Responses


class WSGI_Fake:

    def __call__(self, environ: dict, start_response):
        self.environ = environ

        self.request = Request(self.environ)
        self.responser = Responses()
        start_response('200 OK', [('Content-type', 'text/html')])
        return [bytes('Hello from Fake', encoding='utf-8')]




