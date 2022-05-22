from framework.request import Request
# from url import Url
# from views import Views
from url import links
# GET, POST, PUT, HEAD, DELETE, TRACE, OPTIONS, CONNECT, PATCH


class WSGI:
    def __init__(self, front_controllers: tuple):
        self.front_controllers = front_controllers

    def __call__(self, environ: dict, start_response):
        response = None
        request = Request(environ)

        # front_controller
        if self.front_controllers:
            for front in self.front_controllers:
                response = front(request, self.generate_answer, start_response)
            # return response if response else [b'404']
        else:
            response = self.generate_answer(start_response, request)
        return response if response else [b'404']

    # page_controller
    def generate_answer(self, start_response, req):
        # if req.method in ('GET', 'POST'):
        for custom_url, custom_view in links.items():
            if req.path == custom_url:
                print(f'{req.method=} {req.query_params=}')
                start_response('200 OK', [('Content-Type', 'text/html')])
                return [bytes(f'{custom_view(req)}', encoding='utf-8')]
        # return [bytes(f'unsupported method {req.method}', encoding='utf-8')]
        # elif req.method == 'POST':
        #     for custom_url, custom_view in links.items():
        #         if req.path == custom_url:
        #             start_response('200 OK', [('Content-Type', 'text/html')])
        #             return [bytes(f'{custom_view(req.method)}', encoding='utf-8')]

