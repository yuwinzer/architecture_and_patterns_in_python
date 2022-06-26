from secrets import token_hex

from database import DB as db


class Users:

    # def __init__(self):
    #     self.id: int = 0
    #     self.username: str
    #     self.password: str
    #     self.token: str
    #     self.tel: str
    #     db_mapper.UnitOfWork.new_current()

    #     self.__username: str = ''
    #     self.__password: str = ''
    #     # self.__firstname: str = ''
    #     # self.__lastname: str = ''
    #     self.__tel: str = ''
    #     self.__courses: dict = {}
    #
    # @property
    # def username(self):
    #     return self.__username
    #
    # @username.setter
    # def username(self, username):
    #     if not isinstance(username, str):
    #         print(f'Name must be a string: {username}')
    #     if len(username) < 3 or len(username) > 16:
    #         print(f'Length of username {username} must be 3-16')
    #     self.__username = username
    #
    # @property
    # def password(self):
    #     return self.__password
    #
    # @password.setter
    # def password(self, password):
    #     if not isinstance(password, str):
    #         print(f'Password must be a string: {password}')
    #     if len(password) < 3 or len(password) > 16:
    #         print(f'Length of password {password} must be 3-16')
    #     self.__password = password
    #
    # @property
    # def tel(self):
    #     return self.__tel
    #
    # @tel.setter
    # def tel(self, tel):
    #     if not isinstance(tel, str):
    #         print(f'Tel must be a string: {tel}')
    #     if len(tel) < 7 or len(tel) > 10:
    #         print(f'Length of tel {tel} must be 7-10')
    #     self.__tel = tel
    #
    # @property
    # def courses(self):
    #     return self.__courses
    #
    # @add_course.setter
    def add_course(self, request, _id: int):
        if self.check_course(_id):
            if _id in request.user.courses:
                return
            request.user.courses.append(_id)

    def del_course(self, request, _id):
        if self.check_course(_id):
            if _id in request.user.courses:
                request.user.courses.remove(_id)

    @staticmethod
    def check_course(_id: int):
        if not isinstance(_id, int):
            print(f'Course id must be an integer: {_id}')
            return False
        if _id <= 0:
            print(f'Course id must be higher than 0: {_id}')
            return False
        return True

    # @staticmethod
    # def check_user_token(username: str, token: str):
    #     _user = db.users.get_by('username', username)
    #     if _user:
    #         if _user.token == token:
    #             return True
    #         return False
    #     return None
        # for user in self.database.users:
        #     if user['username'] == username:
        #         # print(f'check_user_token: {user["username"]=} {user["token"]=}')
        #         if user['token'] == token:
        #             return True
        #         return False
        # return None

    # def get_user_max_id(self, username):
    #     max_id = 1
    #     for user in self.database.users:
    #         max_id = max(max_id, user['id'])
    #         if user['username'] == username:
    #             return user, max_id
    #     return None, max_id

    def get_user(self, username: str):
        user = db.users.get_by('username', username)
        # for user in self.database.users:
        if user:
            return user
        return None

    def create_user_from_request(self, request):
        # print(f'{request.body=} {username=}')
        # if 'username' in request.auth and 'password' in request.auth:
        if request.auth is None or \
                'username' not in request.auth or \
                request.auth['username'] == '' \
                'password' not in request.auth or \
                request.auth['password'] == '' \
                'tel' not in request.auth or \
                request.auth['tel'] == '':
            print(f'ERROR on register: В запросе отсутствует(ют) поля : {request.auth=}')
            return False, f'Заполните обязательные поля'
        if not self.has_allowed_symbols(request.auth['username']):
            return False, 'Недопустимые символы в имени<br>Используйте инглиш'
        _user = db.users.get_by('username', (request.auth['username']))
        if not _user:
            _email = request.auth['email'] if 'email' in request.auth else ''
            token = str(token_hex(16))
            db.users.add({'username': request.auth['username'],
                          'password': request.auth['password'],
                          'token': token,
                          'tel': request.auth['tel'],
                          'email': _email})
            request.headers_to_send['HTTP_AUTHORIZATION'] = f'{request.auth["username"]}:{token}'
            return True, f'Добро пожаловать на наш проект, {request.auth["username"]}. Приятной учебы.'
        return False, 'Данное имя уже занято.'

    def login_user(self, request, reg_login: bool = False):
        # print(f'{request.auth=} {type(request.auth)=}')
        if 'username' in request.auth and 'password' in request.auth:
            if not self.has_allowed_symbols(request.auth['username']):
                return False, 'Недопустимые символы в имени<br>Используйте инглиш'
            _user = self.get_user(request.auth['username'])
            if _user:
                if _user.password == request.auth['password']:
                    print(f'LOGIN_USER: {_user.username}')
                    if _user.token == '':
                        _user.token = str(token_hex(16))
                        _user.to_edit()
                        request.user = _user

                    request.headers_to_send['HTTP_AUTHORIZATION'] = f'{_user.username}:{_user.token}'
                    return True, f'Здравствуйте, {_user.username}<br>Добро пожаловать на наши курсы'
                return False, 'Неправильный пароль.'
        return False, 'Аккаунта с таким именем не существует'

    def logout_user(self, request):
        if request.verified:
            try:
                _user = db.users.get_by_id(request.user.id)
                _user.token = ''
                _user.to_edit()
                request.user.token = ''
                request.verified = None
            except Exception as e:
                print(f'Не удалось разлогинить аккаунт {request.username} по причине: {e}')

    @staticmethod
    def has_allowed_symbols(string, lim1: int = 45, lim2: int = 126):
        return all(lim1 <= ord(c) <= lim2 for c in string)


U = Users()
