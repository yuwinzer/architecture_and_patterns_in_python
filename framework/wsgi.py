from os import path

import settings
from database import DB
from framework.request import Request
from framework.responses import Responses
from framework.front_controller import Middleware
from views import View

if path.exists('url.py'):
    from url import links
else:
    links = None


# GET, POST, PUT, HEAD, DELETE, TRACE, OPTIONS, CONNECT, PATCH


class WSGI:

    def __init__(self):
        self.m_ware = Middleware()
        self.m_wares = settings.MIDDLEWARE

    def __call__(self, environ: dict, start_response):
        self.environ = environ
        self.start_response = start_response

        self.request = Request(self.environ)
        self.responser = Responses()
        self.response = None
        # print(f'GOT REQUEST: {self.request=}')
        # print(f'{self.responser=}')

        # Call front_controllers if registered
        if self.m_wares:
            for front in self.m_wares:  # Pre front controllers
                self.response = front(self.m_ware, self.request, self.response, self.responser, True)
            # If middleware does not change status - generate answer
            # Else use middleware status
            self.response = self.generate_answer()
            for front in self.m_wares:  # Post front controllers
                self.response = front(self.m_ware, self.request, self.response, self.responser, False)
        else:
            self.response = self.generate_answer()

        # print(f'{self.response=}')
        # try:
        DB.commit()
        # except Exception as err:
        #     print(f'ERROR while commiting: {err}')
        # print(f'RESPONSE: {self.response}')
        return self.response

    # page_controller
    def generate_answer(self):
        if self.responser.status == '':
            # Search for view under decorator @app
            self.search_url_and_send(View.views)
            # print(f'{self.responser.status=}')
            # Search for view in upl.py -> links
            if links and self.responser.status == '':
                self.search_url_and_send(links)
            if self.responser.status == '':
                self.responser.status_404()

        # print(f'SEND STATUS={self.responser.status=} HEADERS={self.responser.headers=}')
        # print(f'{self.responser.body=}')
        self.start_response(self.responser.status, self.responser.headers)
        return [bytes(f'{self.responser.body}', encoding='utf-8')]

    def search_url_and_send(self, source: dict, status_func: classmethod = None):
        if status_func is None:
            status_func = self.responser.status_200
        for custom_url, custom_view in source.items():
            if self.request.path == custom_url:
                status_func(self.request, custom_view)
                return

