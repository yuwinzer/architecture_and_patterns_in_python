from secrets import token_hex
from framework import db_mapper

from database import DB as db


class Users:

    def __init__(self):
        self.id: int = 0
        self.username: str
        self.password: str
        self.token: str
        self.tel: str
        # db_mapper.UnitOfWork.new_current()

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
    def add_course(self, request, _id):
        if self.check_course(_id):
            if _id in request.user.courses:
                return
            request.user.courses.append(_id)

    def del_course(self, request, _id):
        if self.check_course(_id):
            if _id in request.user['courses']:
                request.user['courses'].remove(_id)

    @staticmethod
    def check_course(__id):
        if not isinstance(__id, int):
            print(f'Course id must be an integer: {__id}')
        if __id <= 0:
            print(f'Course id must be higher than 0: {__id}')
        return True

    @staticmethod
    def check_user_token(username, token):
        user = db.users.get_by('username', username)
        if user:
            if user.token == token:
                return True
            return False
        return None
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

    def get_user(self, username):
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
        _user = db.users.get_by('username', (request.auth['username']))
        if not _user:
            _email = request.auth['email'] if 'email' in request.auth else ''
            token = str(token_hex(16))
            db.users.add({'username': request.auth['username'],
                          'password': request.auth['password'],
                          'token': token,
                          'tel': request.auth['tel'],
                          'email': _email})
            # db_mapper.UnitOfWork.get_current().commit()
            # self.database.users.append({'id': _max_id + 1,
            #                             'username': request.auth['username'],
            #                             'password': request.auth['password'],
            #                             'token': token,
            #                             'tel': request.auth['tel'],
            #                             'email': _email,
            #                             'courses': []})
            request.headers_to_send['HTTP_AUTHORIZATION'] = f'{request.auth["username"]}:{token}'
            return True, f'Добро пожаловать на наш проект, {request.auth["username"]}. Приятной учебы.'
        return False, 'Данное имя уже занято.'

    def login_user(self, request, reg_login: bool = False):
        # print(f'{request.auth=} {type(request.auth)=}')
        # auth = request.reg if reg_login else request.auth
        auth = request.auth
        if 'username' in auth and 'password' in auth:
            _user = self.get_user(auth['username'])
            # print(f'{_user=}')
            if _user:
                if _user.password == auth['password']:
                    if _user.token == '':
                        _user.token = str(token_hex(16))
                        _user.to_edit()
                        request.user = _user
                        # db_mapper.UnitOfWork.get_current().commit()

                    request.headers_to_send['HTTP_AUTHORIZATION'] = f'{_user.username}:{_user.token}'
                    # request.send_headers['HTTP_AUTHORIZATION'] = f'Bearer {_user["username"]}:{_user["token"]}'
                    return True, f'Здравствуйте, {_user.username}<br>Добро пожаловать на наши курсы'
                return False, 'Неправильный пароль.'
        return False, 'Аккаунта с таким именем не существует'

    def logout_user(self, request):
        if request.verified:
            try:
                _user = db.users.get_by_id(request.user.id)
                _user.token = ''
                _user.to_edit()
                # for _user in DB.users:
                #     if _user['username'] == request.username:
                #         _user['token'] = ''
                request.user.token = ''
                request.verified = None
            except Exception as e:
                print(f'Не удалось разлогинить аккаунт {request.username} по причине: {e}')


U = Users()
