from request import Request


def app(environ, start_response):

    request = Request(environ)
    print(request.headers)
    # print(request.body.read())
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'simple_wsgi.py is working']
