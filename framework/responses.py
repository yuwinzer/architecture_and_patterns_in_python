from setup import PAGE_404
from framework.views import View


class Responses:
    def __init__(self):
        self.body: str = ''
        self.status: str = ''
        self.headers: list = []

    def __call__(self):
        self.body = ''
        self.status = ''
        self.headers = []

    def status_200(self, request, custom_view):
        self.status = '200 OK'
        self.body = custom_view(request)
        self.headers = [('Content-type', 'text/html')]
        return self

    def status_404(self):
        self.status = '404 NOT FOUND'
        self.body = View.view(PAGE_404) if PAGE_404 else '<p>404'
        self.headers = [('Content-type', 'text/html')]
        return self
