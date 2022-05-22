from framework.views import view
DIR = 'frontend/'
# DOMEN = '127.0.0.1:8000'

link_vars = {
    '%index%': '"/index"',
    '%about%': '"/about"'
}


def index():
    page = view(DIR+'index.html', link_vars)
    return page


def about():
    page = view(DIR+'about.html', link_vars)
    return page
