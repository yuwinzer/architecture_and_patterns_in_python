from framework.front_controller import Middleware

MIDDLEWARE = (
    Middleware.answer_time,
    Middleware.cors
)
MIDDLEWARE_SETUP = {
    'cors_ip_whitelist': (
        '127.0.0.1',
        '0.0.0.0'
    ),
    'cors_ip_blacklist': (
    )
}
PAGE_404 = ''
