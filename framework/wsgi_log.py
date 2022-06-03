from os import path

import setup
from framework.request import Request
from framework.responses import Responses
from framework.front_controller import Middleware
from views import View
if path.exists('url.py'):
    from url import links
else:
    links = None
# GET, POST, PUT, HEAD, DELETE, TRACE, OPTIONS, CONNECT, PATCH


class WSGI_Log:
    def __init__(self):
        self.m_ware = Middleware()
        self.m_wares = setup.MIDDLEWARE

    def __call__(self, environ: dict, start_response):
        self.environ = environ
        self.start_response = start_response

        self.request = Request(self.environ)
        self.responser = Responses()
        self.response = None
        print(f'Got request: [{self.request.method}]:{self.request.query_params}')
        # print(f'{self.responser=}')

        # Call front_controllers if registered
        if self.m_wares:
            for front in self.m_wares:  # Pre front controllers
                self.response = front(self.m_ware, self.request, self.response, self.responser, True)
            # If middleware does not change status - generate answer
            # Else use middleware status
            # print(f'{self.responser.status=}')
            self.response = self.generate_answer()
            for front in self.m_wares:  # Post front controllers
                self.response = front(self.m_ware, self.request, self.response, self.responser, False)
        else:

            self.response = self.generate_answer()

        # print(f'{self.response=}')
        return self.response

    # page_controller
    def generate_answer(self):
        if self.responser.status == '':
            # Search for view under decorator @app
            for custom_url, custom_view in View.views.items():
                if self.request.path == custom_url:
                    self.responser.status_200(self.request, custom_view)
                    break
            # Search for view in upl.py -> links
            if links and self.responser.status == '':
                for custom_url, custom_view in links.items():
                    if self.request.path == custom_url:
                        self.responser.status_200(self.request, custom_view)
                        break
            if self.responser.status == '':
                self.responser.status_404()

        # print(f'{status=} {headers=}')
        self.start_response(self.responser.status, self.responser.headers)
        return [bytes(f'{self.responser.body}', encoding='utf-8')]




