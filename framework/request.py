class Request:
    def __init__(self, environ: dict):
        self.headers = self._get_http_headers(environ)
        self.method = environ.get('REQUEST_METHOD')
        self.body = environ.get('wsgi.input')
        self.query_params = environ.get('QUERY_STRING')
        self.path = environ.get('PATH_INFO')

    def _get_http_headers(self, environ: dict):
        headers = {}
        for key, value in environ.items():
            if key.startswith('HTTP_'):
                headers[key[5:]] = value
            # else:
                # print('NOT HTTP:', key, value)
        return headers

