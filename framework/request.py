from urllib import parse
from framework.users import U


class Request:
    def __init__(self, environ: dict):
        print('-' * 80)
        self.users = U
        self.act = ''
        self.auth = {}
        self.env = environ
        self.headers = self._get_http_headers()
        self.method = environ.get('REQUEST_METHOD')
        self.body = self._parse_post_query_params()
        print(f'BODY: {self.body}')
        self.query_params = self._get_get_query_params(environ)
        self.path = self._get_clean_path()
        print(f'REQ_PATH: {self.path}')
        self.client_ip4 = environ.get('REMOTE_ADDR')
        self.verified, self.username, self.user = self._check_token()  # True, username, user
        print(f'VERIFIED: {self.verified} {self.username=} {self.user=}')
        self.headers_to_send = {}  # If name/pass verified on login? then Bearer
        self.origin = environ.get('HTTP_ORIGIN')

    def _get_http_headers(self) -> dict:
        headers = {}
        debug = 0
        if debug:
            print('-' * 80)
            for key, value in self.env.items():
                if key.startswith('HTTP_'):
                    headers[key[5:]] = value
                    print('HTTP:', key, value)
                    if key == 'HTTP_AUTHORIZATION':
                        print(f'+++++++++++++++++++++++++++++++++++++++++++++++: {key}, {value}')
                else:
                    print('NOT HTTP:', key, value)
        else:
            for key, value in self.env.items():
                if key.startswith('HTTP_'):
                    headers[key[5:]] = value
        return headers

    def _check_token(self) -> tuple[None, None, None] | tuple[bool, str, type(U)]:
        auth = self.env.get('HTTP_AUTHORIZATION')
        # print(f'{self.act=} {auth=}')
        _username, _token = self._parse_auth_header(auth)
        if _username:
            _user = self.users.get_user(_username)
            if _user:
                if _user.token == _token:
                    # print(f'{_username=}')
                    return True, _username, _user
                return False, _username, _user

        elif self.act in ('login', 'reg'):
            _user = self.users.get_user(self.auth['username'])
            if _user:
                return True, self.auth['username'], _user

        return None, None, None

    @staticmethod
    def _parse_auth_header(auth) -> tuple[None, None] | tuple[str, str]:
        if auth:
            if auth.startswith("Bearer ") and ':' in auth[7:]:
                _username, _token = (auth[7:].split(':'))
                return _username, _token
        return None, None

    def _get_get_query_params(self, environ: dict) -> dict | None:
        data = parse.unquote(environ.get('QUERY_STRING'))
        if not data:
            return
        return self._parse_query(data, '&')

    def _parse_post_query_params(self) -> dict | None:
        body = parse.unquote(self.env.get('wsgi.input').read().decode("utf-8"))
        if not body:
            return
        elif '\r\n' in body:
            parsed_body = self._parse_query(body, '\r\n')
        elif '&' in body:
            parsed_body = self._parse_query(body, '&')
        else:
            return
        self._set_auth_from_parsed_body(parsed_body)
        return parsed_body

    def _set_auth_from_parsed_body(self, parsed_body: dict) -> None:
        if 'act' in parsed_body:
            if parsed_body['act'] == 'login':
                if 'uname' in parsed_body and 'pass' in parsed_body:
                    self.act = 'login'
                    self.auth['username'] = parsed_body['uname']
                    self.auth['password'] = parsed_body['pass']
            elif parsed_body['act'] == 'reg':
                if 'uname' in parsed_body and \
                        'pass' in parsed_body and \
                        'tel' in parsed_body:
                    self.act = 'reg'
                    self.auth['username'] = parsed_body['uname']
                    self.auth['password'] = parsed_body['pass']
                    self.auth['tel'] = parsed_body['tel']

    @staticmethod
    def _parse_query(data: str, terminator: str) -> dict | None:
        query_params = {}
        # print(f'{data=}')
        pair = ''
        try:
            for pair in data.split(terminator):
                if not pair:
                    continue
                separ = pair.find('=')
                var, value = pair[:separ], pair[separ + 1:]
                if query_params.get(var):
                    if isinstance(query_params[var], list):
                        query_params[var].append(value)
                    else:
                        query_params[var] = [query_params[var]]
                        query_params[var].append(value)
                else:
                    query_params[var] = value
        except Exception as e:
            print(f"ERROR: Can't parse request: {e}: {data} {pair=}")
            return
        return query_params

    def _get_clean_path(self) -> str:
        path = self.env.get('PATH_INFO')
        if len(path) > 1 and path.endswith('/'):
            return path[:-1]
        return path
