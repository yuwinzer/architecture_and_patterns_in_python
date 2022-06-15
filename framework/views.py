import os
import sys
from time import time
from functools import wraps


class View:
    views = {}

    def __init__(self,
                 frontend_path: str = 'frontend',
                 frontend_vars: dict = None,
                 frontend_admin_vars: dict = None,
                 deepness: int = 1):
        self.frontend_path = frontend_path
        self.frontend_vars = frontend_vars
        self.frontend_admin_vars = frontend_admin_vars
        self.deepness = deepness
        self.is_admin = False

        self.injections = None
        self.query_params = None
        self.file_name = None

    def view(self, page_file: str = 'index.html', injections=None, query_params=None):
        self._apply_to_self(injections, query_params)
        try:
            with open(f'{self.frontend_path}{page_file}', 'r') as file:
                data = file.read().replace('\n', '').replace('    ', ' ')
            # Заменяем {{переменные}} и циклы на содержимое из внешних файлов
            data, _ = self._just_inject_in_that_file(data, page_file)
            # Заменяем %константы% на константы пользователя
            for var, link in self.frontend_vars.items():
                data = data.replace(var, link)
            for var, link in self.frontend_admin_vars.items():
                data = data.replace(var, link if self.is_admin else '')

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f'{fname}[{exc_tb.tb_lineno}]ERROR: while parsing view: ({page_file=}) {e}')
            return page_file
        return data

    # Рекурсивно-костыльный шаблонизатор. С JINJA не разбирался, интересно было написать свой
    def _just_inject_in_that_file(self, html_data, file: str, num: int = 0):
        try:
            stopper = 0
            layer = 0
            inj_end = 0
            data = str(html_data) if isinstance(html_data, int) else html_data
            data = self._remove_comments(data, file)
            while layer < self.deepness:

                # print(f'Using layer {layer} of {self.deepness}')
                inj_start = data.find('{{', inj_end)
                if inj_start >= 0:
                    inj_end = data.find('}}', inj_start)
                    if inj_end == -1:
                        raise Exception(f'ERROR: not found "}}" in {file}')
                    inj_var = data[inj_start + 2: inj_end]
                    if len(inj_var) <= 1:
                        continue
                    # print(f'{inj_var=} {inj_start=} {inj_end=}')
                    # CYCLES. If * found, then content will repeat
                    cycle_pos = inj_var.find('*')
                    if cycle_pos >= 0:
                        cycle_end = data.find('{{*}}', inj_end)
                        cycle_data = data[inj_end + 2:cycle_end]
                        cycles = int(inj_var[cycle_pos + 1:])
                        cycle_var = inj_var[:cycle_pos]
                        cycle_dig = 0

                        if cycle_var.isdigit():
                            cycle_dig = int(cycle_var)
                        else:
                            _cycle_var = self._get_value_from_injections(cycle_var)
                            if _cycle_var:
                                if isinstance(_cycle_var, int):
                                    cycle_dig = _cycle_var
                                elif isinstance(_cycle_var, str) and _cycle_var.isdigit():
                                    cycle_dig = int(cycle_var)
                                else:
                                    print(f'views.py ERROR: unknown variable <{cycle_var}> '
                                          f'in ({file}) while expected digit or key if digit')
                        cycles_data = ''
                        # print(f'{inj_var=} {cycles=} {cycle_var=} {cycle_dig=} {cycle_data=} ')
                        for i in range(0, cycles):
                            # print(f'cycle start: {i}  id:{cycle_dig + i}')
                            cd, stopper = self._just_inject_in_that_file(cycle_data, file, cycle_dig + i)
                            if stopper:
                                break
                            cycles_data += cd
                            # print(f'cycle end: {i} {cycle_data=}')
                        inj_end = cycle_end + 3
                        data = data[:inj_start] + cycles_data + data[inj_end + 2:]
                        # print(f'CYCLES ENDED: {data=}')
                        continue
                    inj_arg, key = None, None

                    # if injections not empty:
                    # If inj_var is key, inject directly
                    if self.injections:
                        inj_arg = self._get_value_from_injections(inj_var)
                        # print(f'FOUND {inj_var=} {inj_arg=}')

                    if inj_arg is None:
                        # If : found, then injection parse dictionary <dict:key>
                        inj_arg, key = self._try_parse_dict(inj_var)

                    if inj_arg is None:
                        # If # found, then get number (for list, etc.) <object#number>
                        inj_arg, num = self._try_parse_numeric(inj_var, num)

                    # print(f'{inj_var=} {type(inj_arg)=}')
                    # print(f'{inj_arg=}')
                    if inj_arg is not None:
                        file = inj_arg
                        if isinstance(inj_arg, int):
                            inj_data = str(inj_arg)
                            # print(f'INT {inj_data=}')
                        elif isinstance(inj_arg, str):
                            if inj_arg[-5:] == '.html':  # If str.html, then filename
                                inj_data = self._open_file(f'{self.frontend_path}{inj_arg}')
                            else:
                                inj_data = inj_arg
                        elif isinstance(inj_arg, list):
                            if num < len(inj_arg):
                                # print(f'{num=} {len(inj_arg)=} {inj_arg[num - 1]["id"]=}')
                                inj_data = inj_arg[num][key]
                                if num == len(inj_arg):
                                    stopper = 1
                                # print(f'{num=} {inj_arg[num][key]=}')
                            else:
                                stopper = 1
                                inj_data = ''
                                data = ''

                        elif isinstance(inj_arg, dict):
                            if key in inj_arg:
                                inj_data = inj_arg[key]
                        elif isinstance(inj_arg, tuple):
                            print('tuple')
                        else:
                            print(f'ATTENTION: unknown type var: ({inj_var=} {type(inj_arg)=})'
                                  f' in ({file if isinstance(file, str) else "injection"})')
                            inj_data = ''
                    elif inj_var[-5:] == '.html':  # If not variable, then filename
                        inj_data = self._open_file(f'{self.frontend_path}{inj_var}')
                    else:
                        print(f'ATTENTION: unused var: ({inj_var=})'
                              f' in ({file if isinstance(file, str) else "injection"})')
                        # print(f'{data=}')
                        inj_data = ''
                        data = ''
                    if layer < self.deepness:
                        inj_data, _ = self._just_inject_in_that_file(inj_data, file, num)
                    data = data[:inj_start] + inj_data + data[inj_end + 2:]
                    # print(f'{data =}')
                    # print(f'{inj_var=} {inj_file=}')
                else:
                    layer += 1
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f'{fname}[{exc_tb.tb_lineno}]ERROR: while parsing view: ({file}) {e}')
        return data, stopper

    def _remove_comments(self, html_data: str, file: str):
        html_result = ''
        data_start = 0
        while True:
            data_end = html_data.find('<!--', data_start)
            if data_end >= 0:
                html_result = f'{html_result}{html_data[data_start: data_end]}'
                # print(f'|||{data_start=} {data_end=} {html_result=} {html_data[data_start: data_end]=}')
                data_start = html_data.find('-->', data_end)
                if data_start >= 0:
                    data_start += 3
                else:
                    print(f'ATTENTION: broken comment in ({file if isinstance(file, str) else "injection"})')
                    break
            else:
                break
        html_result = f'{html_result}{html_data[data_start:]}'
        return html_result

    def _try_parse_dict(self, inj_var):
        dot_pos = inj_var.find(':')
        if dot_pos >= 0:
            obj = inj_var[:dot_pos]
            key = inj_var[dot_pos + 1:]
            # print(f'{key=} {arg=}')
            inj_arg = self._get_value_from_injections(obj)
            return inj_arg, key
        return None, None

    def _try_parse_numeric(self, inj_var, num):
        dot_pos = inj_var.find('#')
        if dot_pos >= 0:
            obj = inj_var[:dot_pos]
            repeater = inj_var[dot_pos + 1:]
            if repeater.isdigit():
                num = int(repeater)
            else:
                repeater = self._get_value_from_injections(repeater)
            # elif repeater in self.injections.keys():
            #     num = self.injections[repeater]
            if repeater:
                num = repeater
            # print(f'{obj=} {num=}')
            inj_arg = self._get_value_from_injections(obj)
            return inj_arg, num
        return None, None

    def _apply_to_self(self, injections, query_params):
        if injections is None:
            injections = {}
        self.injections = injections
        if query_params is None:
            query_params = {}
        self.query_params = query_params

    def _get_value_from_injections(self, key: str):
        if key in self.injections.keys():
            return self.injections[key]
        return None

    def _open_file(self, path):
        with open(path, 'r') as file:
            data = file.read().replace('\n', '').replace('    ', ' ')
            data = self._remove_comments(data, path)
            return data

    def path(self, file_name: str):
        return f'{self.frontend_path}{file_name}'


def app(url: str = ''):
    def route(func: type):
        View.views[url] = func
        return func
    return route


def debug(func):
    @wraps(func)
    def decor(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        print(f'Execution: "{func.__module__}->{func.__name__}" Time taken: {(time() - start_time).__round__(6)}')
        return result

    return decor
