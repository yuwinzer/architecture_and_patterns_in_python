from framework.wsgi import WSGI
from framework import front_controller

front_controllers = (
    # front_controller.get_time,
)

app = WSGI(front_controllers)
