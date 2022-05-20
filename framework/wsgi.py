from framework.request import Request
# from url import Url
# from views import Views
from url import links
# GET, POST, PUT, HEAD, DELETE, TRACE, OPTIONS, CONNECT, PATCH


class WSGI:

    def app(self, environ: dict, start_response, front_controllers: tuple):
        response = None
        req = Request(environ)

    # front_controller
        for front in front_controllers:
            response = front(req, self.generate_answer, start_response)
        return response if response else [b'404']

    # page_controller
    def generate_answer(self, start_response, req):
        if req.method == 'GET':
            for url, method in links.items():
                if req.path == url:
                    start_response('200 OK', [('Content-Type', 'text/html')])
                    return [bytes(f'{method()}', encoding='utf-8')]
