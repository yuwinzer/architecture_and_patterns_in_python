from framework import db_mapper


class Database:
    # db_mapper.UnitOfWork.new_current()
    # users = db_mapper.Table('users')
    # courses = db_mapper.Table('courses')
    # lines = db_mapper.Table('lines')
    # types = db_mapper.Table('line_types')

    def __init__(self):
        db_mapper.UnitOfWork.new_current()
        self.users = db_mapper.Table('users')
        self.courses = db_mapper.Table('courses')
        self.lines = db_mapper.Table('lines')
        self.types = db_mapper.Table('line_types')

    def commit(self):
        print(f'{db_mapper.UnitOfWork.get_current()=}')
        # if db_mapper.UnitOfWork.get_current():
        db_mapper.UnitOfWork.get_current().commit()
    # def add(self, data):
    #     db_mapper.Row(self, data)

    # def db_get_line(self, _id):
    #     _id = self._to_int(_id)
    #     for _elem in self.course_lines:
    #         if _elem['id'] == _id:
    #             return _elem
    #     return None

    def get_lines_by_parent(self, _id):
        _lines = self.lines.get_list_by('parent', _id)
        return _lines

    # def get_courses_by_parent(self, _id):
    #     _courses = self.courses.get_list_by('parent', _id)
    #     return _courses

    # def db_get_all_lines(self):
    #     return self.course_lines

    # def db_get_course(self, _id):
    #     _id = self._to_int(_id)
    #     for _elem in self.courses:
    #         if _elem['id'] == _id:
    #             _elem['type'] = self.db_get_type(_elem['type'])
    #             # print(f'{__elem=}')
    #             return _elem
    #     return None

    # def db_get_courses_by_line(self, _line):
    #     _line = self._to_int(_line)
    #     _res = [_elem for _elem in self.courses if _elem['line'] == _line]
    #     for _elem in _res:
    #         for _t in self.course_types:
    #             if _t['id'] == _elem['type']:
    #                 _elem['type'] = _t['name']
    #                 break
    #     return _res

    # def db_get_course_amt_by_line(self, _line) -> int:
    #     # line = _to_int(line)
    #     _count = 0
    #     for _elem in self.courses:
    #         if _elem['line'] == _line:
    #             _count = _count + 1
    #     # print(f'{count=}')
    #     return _count

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

    # @staticmethod
    # def _to_int(_var):
    #     # print(f'{type(var)=}')
    #     if not _var:
    #         return 1
    #     return _var if isinstance(_var, int) else int(_var)
    
    
    # def db_get_all_users():
    #     # id = _to_int(id)
    #     if user in users.keys():
    #         return users[id]
    #     return None
    
DB = Database()
