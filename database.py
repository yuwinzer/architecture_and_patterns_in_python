class Database:
    def __init__(self):
        self.course_types = (
            {'id': 1, 'name': 'онлайн'},
            {'id': 2, 'name': 'офлайн'},
        )

        self.course_lines = [
            {'id': 1, 'parent': 0, 'courses_in': 0, 'name': 'Программирование'},
            {'id': 2, 'parent': 0, 'courses_in': 0, 'name': 'Электроника'},
            {'id': 3, 'parent': 0, 'courses_in': 0, 'name': 'Учимся жить'},

            {'id': 4, 'parent': 1, 'courses_in': 0, 'name': 'Базовые знания'},
            {'id': 13, 'parent': 1, 'courses_in': 0, 'name': 'Логика'},
            {'id': 5, 'parent': 1, 'courses_in': 0, 'name': 'Языки высокого уровня'},
            {'id': 6, 'parent': 1, 'courses_in': 0, 'name': 'Языки низкого уровня'},

            {'id': 14, 'parent': 5, 'courses_in': 0, 'name': 'Python'},
            {'id': 15, 'parent': 5, 'courses_in': 0, 'name': 'Java'},
            {'id': 16, 'parent': 5, 'courses_in': 0, 'name': 'JavaScript'},
            {'id': 17, 'parent': 5, 'courses_in': 0, 'name': 'Kotlin'},

            {'id': 18, 'parent': 6, 'courses_in': 0, 'name': 'Assembler'},
            {'id': 19, 'parent': 6, 'courses_in': 0, 'name': 'C'},
            {'id': 20, 'parent': 6, 'courses_in': 0, 'name': 'C++'},

            {'id': 7, 'parent': 2, 'courses_in': 0, 'name': 'Базовые элементы и понятия'},
            {'id': 8, 'parent': 2, 'courses_in': 0, 'name': 'Схемотехника'},
            {'id': 9, 'parent': 2, 'courses_in': 0, 'name': 'Ремонт электроники'},

            {'id': 10, 'parent': 3, 'courses_in': 0, 'name': 'Добрые дела'},
            {'id': 11, 'parent': 3, 'courses_in': 0, 'name': 'Выгодные дела'},
            {'id': 12, 'parent': 3, 'courses_in': 0, 'name': 'Безделье'},
        ]

        self.courses = [
            {
                'id': 1, 'line': 10, 'name': 'Как перевести бабушку через дорогу', 'img': 'img:старушка', 'type': 1,
                'short': 'Обучает обходительному поведению. Объясняет все риски при контакте с бабушками',
                'text': 'После прохождения данного курса вы больше не сможете устоять и проведете бабушку через дорогу'
            },
            {
                'id': 2, 'line': 10, 'name': 'Как уступить место в транспорте', 'img': 'img:трамвай', 'type': 1,
                'short': 'У вас пропадет желание садиться. Узнаете альтернативные способы передвижения',
                'text': 'После прохождения данного курса вы больше не сможете сидеть и научитесь ходить'
            },
            {
                'id': 3, 'line': 10, 'name': 'Как покормить голубей', 'img': 'img:голуби', 'type': 2,
                'short': 'Научит убегать от копов, бомжей и зомби. Дополнительно информация о птичьем ГРИППе',
                'text': 'После прохождения данного курса вы больше не захотите кормить голубей. Так же повысится выживаемость'
            },
            {
                'id': 4, 'line': 10, 'name': 'Как заставить себя пойти на выборы', 'img': 'img:галочка', 'type': 2,
                'short': 'Узнаете что такое выборы и влияют ли они на что-то в вашей стране',
                'text': 'После прохождения данного курса вы скорее всего смените гражданство. Если это еще возможно.'
            },
            {
                'id': 5, 'line': 10, 'name': 'Как не лениться делать уборку', 'img': 'img:веник', 'type': 1,
                'short': 'Обучает базовым навыкам владения роботом-пылесосом',
                'text': 'После прохождения данного курса вы без труда найдете кнопку включения'
            },
            {
                'id': 6, 'line': 11, 'name': 'Как приручить соседа', 'img': 'img:лицо соседа', 'type': 1,
                'short': 'Обучает обрастать полезными связями. Объясняет все риски при контакте с соседом',
                'text': 'После прохождения данного курса вы больше не сможете устоять и пригласите соседа выпить'
            },
            {
                'id': 7, 'line': 11, 'name': 'Как заработать миллион за 15 минут', 'img': 'img:777', 'type': 2,
                'short': 'Обучает как быстро заработать и перейти на курс ничегонеделанья',
                'text': 'После прохождения данного курса вы больше не сможете купить другие курсы'
            },
            {
                'id': 8, 'line': 14, 'name': 'Основы Python', 'img': 'img:69', 'type': 2,
                'short': 'Обучает всякой всячине',
                'text': 'После прохождения данного курса вы больше не сможете сесть за другие языки'
            },
            {
                'id': 9, 'line': 14, 'name': 'Продвинутый Питон', 'img': 'img:96', 'type': 2,
                'short': 'Обучает как типизировать руками, магическим методам и type-ам мира сия',
                'text': 'После прохождения данного курса вы сможете превращать 5 строк в 1.'
                        'Но придется превращать 5 строк в 10 классов.'
            },
            {
                'id': 10, 'line': 14, 'name': 'Бог Питона', 'img': 'img:8', 'type': 2,
                'short': 'Обучает познанию сути всего',
                'text': 'После прохождения данного курса вы сможете написать "Hello World" '
                        'без использования абстрактных классов.'
            },
            {
                'id': 11, 'line': 18, 'name': 'Как полюбить регистры', 'img': 'img:AX BX CX DX', 'type': 2,
                'short': 'Обучает как не заработать клаустрофобию в стеке',
                'text': 'После прохождения данного курса вы больше не сможете 1101 0110 1100'
            },
            {
                'id': 12, 'line': 19, 'name': 'Поход в музей', 'img': 'img:BORLAND', 'type': 2,
                'short': 'Исторический курс',
                'text': 'После прохождения данного курса вам стоит пройти Паскаль'
            },
            {
                'id': 13, 'line': 1, 'name': 'История программирования', 'img': 'img:АРИФМОМЕТР', 'type': 2,
                'short': 'Исторический курс как человечество пришло к созданию первого языка',
                'text': 'Программирование от хардвара до хардкода'
            },
            {
                'id': 14, 'line': 6, 'name': 'История машинного кода', 'img': 'img:ПЕРФАЛЕНТА', 'type': 2,
                'short': 'Исторический курс как человечество скатилось от машинного кода к первому языку',
                'text': 'Машинный код - личинка ассемблера. Ладно, мне просто надо много курсов для теста.'
            },
        ]

        self.users = [
            {'id': 1, 'username': 'Basil', 'password': 'juAevLtnbBX1ZSzf7VbqHsxwAgRmtNdvLWzpsfEEuzE=', 'token': '', 'tel': '555-55-55', 'courses': []},
            {'id': 2, 'username': 'Peter', 'password': 'S//u5C6dqSdsWPyTTkXKwzm2CTaExAAnn4UtIcBs3Ho=', 'token': '', 'tel': '555-55-55', 'courses': []},
        ]
        
    def db_get_line(self, _id):
        _id = self._to_int(_id)
        for _elem in self.course_lines:
            if _elem['id'] == _id:
                return _elem
        return None

    def db_get_lines(self, _id):
        _id = self._to_int(_id)
        _lines = []
        for _elem in self.course_lines:
            if _elem['parent'] == _id:
                _lines.append(_elem)
        return _lines

    def db_get_all_lines(self):
        return self.course_lines

    def db_get_course(self, _id):
        _id = self._to_int(_id)
        for _elem in self.courses:
            if _elem['id'] == _id:
                _elem['type'] = self.db_get_type(_elem['type'])
                # print(f'{__elem=}')
                return _elem
        return None

    def db_get_courses_by_line(self, _line):
        _line = self._to_int(_line)
        _res = [_elem for _elem in self.courses if _elem['line'] == _line]
        for _elem in _res:
            for _t in self.course_types:
                if _t['id'] == _elem['type']:
                    _elem['type'] = _t['name']
                    break
        return _res

    def db_get_course_amt_by_line(self, _line) -> int:
        # line = _to_int(line)
        _count = 0
        for _elem in self.courses:
            if _elem['line'] == _line:
                _count = _count + 1
        # print(f'{count=}')
        return _count

    def db_precount_courses_for_lines(self):

        def db_count_curses_in_branch(_id: int = 0, _amt: int = 0) -> int:
            for _lin in self.course_lines:
                if _lin['parent'] == _id:
                    _amt += db_count_curses_in_branch(_lin['id'], _lin['courses_in'])
                    # print(f'NAME: {line["name"]} AMT:{amt} courses_in:{line["courses_in"]}')
            return _amt

        for _line in self.course_lines:
            _amt_d = self.db_get_course_amt_by_line(_line["id"])  # Count gourses exact line
            _line['courses_in'] = _amt_d
            # print(f'PRE -- NAME: {line["name"]} AMT_D:{amt_d}')
        for _line in self.course_lines:
            _line['courses_in'] += db_count_curses_in_branch(_line['id'])

    def db_get_type(self, _id):
        # id = _to_int(id)
        for _elem in self.course_types:
            if _elem['id'] == _id:
                return _elem
        return self.course_types[0]['name']

    @staticmethod
    def _to_int(_var):
        # print(f'{type(var)=}')
        if not _var:
            return 1
        return _var if isinstance(_var, int) else int(_var)
    
    
    # def db_get_all_users():
    #     # id = _to_int(id)
    #     if user in users.keys():
    #         return users[id]
    #     return None
    
DB = Database()
