from framework.wsgi import WSGI
from framework.wsgi_log import WSGI_Log
from framework.wsgi_fake import WSGI_Fake

app = WSGI()
app_log = WSGI_Log()
app_fake = WSGI_Fake()
