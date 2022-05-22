from dataclasses import dataclass
# from framework.wsgi import WSGI
# from views import Views


@dataclass
class Url:
    # path: str
    # controller: object
    # view: classmethod = WSGI.views
    links: dict
