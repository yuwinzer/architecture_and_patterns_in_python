from framework.wsgi import WSGI
from framework import front_controller

server = WSGI()

front_controllers = (
    front_controller.get_time,
)


def run(environ, start_response):
    return server.app(environ, start_response, front_controllers)
