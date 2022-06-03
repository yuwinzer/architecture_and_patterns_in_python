def db_get_line(id):
    id = _to_int(id)
    for elem in database_course_lines:
        if elem['id'] == id:
            return elem
    return None


def db_get_lines(id):
    id = _to_int(id)
    lines = []
    for elem in database_course_lines:
        if elem['parent'] == id:
            lines.append(elem)
    return lines


def db_get_all_lines():
    return database_course_lines


def db_get_course(id):
    id = _to_int(id)
    for elem in database_courses:
        if elem['id'] == id:
            elem['type'] = db_get_type(elem['type'])
            # print(f'{elem=}')
            return elem
    return None


def db_get_courses_by_line(line):
    line = _to_int(line)
    res = [elem for elem in database_courses if elem['line'] == line]
    for elem in res:
        for t in database_course_types:
            if t['id'] == elem['type']:
                elem['type'] = t['name']
                break
    return res


def db_get_course_amt_by_line(line) -> int:
    line = _to_int(line)
    count = 0
    for elem in database_courses:
        if elem['line'] == line:
            count = count + 1
    # print(f'{count=}')
    return count


def db_count_curses_in_line(id: int, amt: int = 0) -> int:
    id = _to_int(id)
    # amt += db_get_course_amt_by_line(id)
    # print(f'{amt=} {id=}')
    for line in database_course_lines:
        # print(f'FOUND:{line["parent"]=} ANS:{amt=}')
        if line['parent'] == id:
            # print(f'FOUND:{line["id"]} ANS:{id}')
            # amt += db_count_curses_in_line(line['id'], amt)
            amt += db_get_course_amt_by_line(line["id"])
    # print(f'{amt=}')
    return amt


def db_get_type(id):
    # id = _to_int(id)
    for elem in database_course_types:
        if elem['id'] == id:
            return elem
    return database_course_types[0]['name']


def _to_int(var):
    # print(f'{type(var)=}')
    if not var:
        return 1
    return var if isinstance(var, int) else int(var)


database_course_types = (
    {'id': 1, 'name': 'онлайн'},
    {'id': 2, 'name': 'офлайн'},
)


database_course_lines = (
    {'id': 1, 'parent': 0, 'name': 'Программирование'},
    {'id': 2, 'parent': 0, 'name': 'Электроника'},
    {'id': 3, 'parent': 0, 'name': 'Учимся жить'},

    {'id': 4, 'parent': 1, 'name': 'Базовые знания'},
    {'id': 13, 'parent': 1, 'name': 'Логика'},
    {'id': 5, 'parent': 1, 'name': 'Языки высокого уровня'},
    {'id': 6, 'parent': 1, 'name': 'Языки низкого уровня'},

    {'id': 14, 'parent': 5, 'name': 'Python'},
    {'id': 15, 'parent': 5, 'name': 'Java'},
    {'id': 16, 'parent': 5, 'name': 'JavaScript'},
    {'id': 17, 'parent': 5, 'name': 'Kotlin'},

    {'id': 18, 'parent': 6, 'name': 'Assembler'},
    {'id': 19, 'parent': 6, 'name': 'C'},
    {'id': 20, 'parent': 6, 'name': 'C++'},


    {'id': 7, 'parent': 2, 'name': 'Базовые элементы и понятия'},
    {'id': 8, 'parent': 2, 'name': 'Схемотехника'},
    {'id': 9, 'parent': 2, 'name': 'Ремонт электроники'},

    {'id': 10, 'parent': 3, 'name': 'Добрые дела'},
    {'id': 11, 'parent': 3, 'name': 'Выгодные дела'},
    {'id': 12, 'parent': 3, 'name': 'Безделье'},
)

database_courses = (
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
)