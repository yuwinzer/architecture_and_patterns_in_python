from framework import db_mapper as db

users_fields = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE',
    'username': 'VARCHAR (32) NOT NULL UNIQUE',
    'password': 'VARCHAR (44) NOT NULL',
    'token': 'VARCHAR (32)',
    'tel': 'VARCHAR (16)',
    'email': 'VARCHAR (32)'
}

users_data = [
    {'username': 'Basil', 'password': 'juAevLtnbBX1ZSzf7VbqHsxwAgRmtNdvLWzpsfEEuzE=', 'token': '',
     'tel': '555-55-55'},
    {'username': 'Peter', 'password': 'S//u5C6dqSdsWPyTTkXKwzm2CTaExAAnn4UtIcBs3Ho=', 'token': '',
     'tel': '555-55-55'},
]

courses_fields = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE',
    'line': 'SMALLINT NOT NULL',
    'name': 'VARCHAR (64) NOT NULL',
    'img': 'VARCHAR (64)',
    'type': 'TINYINT',
    'short': 'VARCHAR (64)',
    'text': 'TEXT'
}

courses_data = [
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

courses_users_fields = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE',
    'course_id': 'INTEGER NOT NULL',
    'user_id': 'INTEGER NOT NULL',
}

courses_users_data = [
    # {'id': 1, 'name': 'онлайн'},
    # {'id': 2, 'name': 'офлайн'},
]

course_types_fields = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE',
    'name': 'VARCHAR (64)'
}

course_types_data = [
    {'id': 1, 'name': 'онлайн'},
    {'id': 2, 'name': 'офлайн'},
]

course_lines_fields = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE',
    'parent': 'INTEGER',
    'courses_in': 'INTEGER',
    'name': 'VARCHAR (64)'
}

course_lines_data = [
    {'id': 1, 'parent': 0, 'courses_in': 0, 'name': 'Программирование'},
    {'id': 2, 'parent': 0, 'courses_in': 0, 'name': 'Электроника'},
    {'id': 3, 'parent': 0, 'courses_in': 0, 'name': 'Учимся жить'},

    {'id': 4, 'parent': 1, 'courses_in': 0, 'name': 'Базовые знания'},
    {'id': 5, 'parent': 1, 'courses_in': 0, 'name': 'Языки высокого уровня'},
    {'id': 6, 'parent': 1, 'courses_in': 0, 'name': 'Языки низкого уровня'},

    {'id': 7, 'parent': 2, 'courses_in': 0, 'name': 'Базовые элементы и понятия'},
    {'id': 8, 'parent': 2, 'courses_in': 0, 'name': 'Схемотехника'},
    {'id': 9, 'parent': 2, 'courses_in': 0, 'name': 'Ремонт электроники'},

    {'id': 10, 'parent': 3, 'courses_in': 0, 'name': 'Добрые дела'},
    {'id': 11, 'parent': 3, 'courses_in': 0, 'name': 'Выгодные дела'},
    {'id': 12, 'parent': 3, 'courses_in': 0, 'name': 'Безделье'},
    {'id': 13, 'parent': 1, 'courses_in': 0, 'name': 'Логика'},

    {'id': 14, 'parent': 5, 'courses_in': 0, 'name': 'Python'},
    {'id': 15, 'parent': 5, 'courses_in': 0, 'name': 'Java'},
    {'id': 16, 'parent': 5, 'courses_in': 0, 'name': 'JavaScript'},
    {'id': 17, 'parent': 5, 'courses_in': 0, 'name': 'Kotlin'},

    {'id': 18, 'parent': 6, 'courses_in': 0, 'name': 'Assembler'},
    {'id': 19, 'parent': 6, 'courses_in': 0, 'name': 'C'},
    {'id': 20, 'parent': 6, 'courses_in': 0, 'name': 'C++'},
]


def insert_data_to_rows(table, data):
    for elem in data:
        table.add(elem)


db.UnitOfWork.new_current()
users = db.Table('users', users_fields, True)
courses = db.Table('courses', courses_fields, True)
courses_users = db.Table('courses_users', courses_users_fields, True)
lines = db.Table('lines', course_lines_fields, True)
types = db.Table('line_types', course_types_fields, True)

insert_data_to_rows(users, users_data)
insert_data_to_rows(courses, courses_data)
insert_data_to_rows(courses_users, courses_users_data)
insert_data_to_rows(lines, course_lines_data)
insert_data_to_rows(types, course_types_data)


db.UnitOfWork.get_current().commit()
