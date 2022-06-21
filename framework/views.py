import os
import sys
from time import time
from functools import wraps
from settings import DEEPNESS, FRONTEND_PATH


class View:
    views = {}

    def __init__(self,
                 # frontend_path: str = 'frontend',
                 frontend_const: dict = None):
        # self.frontend_path = frontend_path
        self.frontend_const = frontend_const
        self.frontend_vars = {}
        # self.frontend_admin_vars = frontend_admin_vars
        # self.deepness = DEEPNESS
        self.is_admin = False

        self.injections = None
        self.query_params = None
        self.file_name = None

        # self.iterable_starter = 0

        self.error = 0
        self.max_errors = 3

    def view(self, request=None, page_file: str = 'index.html', injections=None, query_params=None):
        self.error = 0
        # self.iterable_starter = 0
        self._apply_to_self(injections, query_params)
        if request.verified:
            # print(f'VERIFIED: {request.verified=}')
            self.injections['verified'] = True
            self.injections['username'] = request.username
        try:
            with open(self.path(page_file), 'r') as file:
                data = file.read().replace('\n', '').replace('    ', ' ')
            # Заменяем {{переменные}} и циклы на содержимое из внешних файлов
            data, _ = self._just_inject_in_that_file(data, page_file)
            # Заменяем %константы% на константы пользователя
            for var, link in self.frontend_const.items():
                data = data.replace(var, link)
            # for var, link in self.frontend_admin_vars.items():
            #     data = data.replace(var, link if self.is_admin else '')

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f'{fname}[{exc_tb.tb_lineno}]ERROR: while parsing view: ({page_file=}) {e}')
            self.error += 1
            return '500'
        # print(f'====DATA: {data}')
        return data

    # Рекурсивно-костыльный шаблонизатор. С JINJA не разбирался, интересно было написать свой
    def _just_inject_in_that_file(self, html_data, file: str, num: int = 0):
        try:
            stopper = 0
            layer = 0
            inj_end = 0
            if isinstance(html_data, int):
                data = str(html_data)
            elif isinstance(html_data, list):
                data = str(html_data)
            else:
                data = html_data
            data = self._remove_comments(data, file)
            # data = self._remove_comments(data, file) if isinstance(html_data, str) else html_data
            while layer <= DEEPNESS:

                # print(f'LAYER: {layer}')
                # print(f'DATA: {data}')  # {data[inj_end:]}')
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
                    no, data, inj_end = self._try_parse_cycle(inj_var, inj_start, inj_end, data, file)
                    if no:
                        continue
                    # CONDITIONS. If ? found, then content will execute on condition
                    no, data, inj_end = self._try_parse_condition(inj_var, inj_start, inj_end, data, file)
                    if no:
                        continue
                    # else:
                    #     layer -= 1

                    inj_arg, key = None, None

                    # if injections not empty:
                    # If inj_var is key, inject directly
                    if self.injections or self.frontend_vars:
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
                                inj_data = self._open_file(self.path(inj_arg))
                            else:
                                inj_data = inj_arg
                        elif isinstance(inj_arg, list):
                            # print(f'NUM: {type(num)=} {num=}')
                            if num < len(inj_arg):
                                # print(f'{num=} {key=} {len(inj_arg)=} {inj_arg[num]["id"]=}')
                                inj_data = inj_arg[num][key]
                                if num == len(inj_arg):
                                    stopper = 1
                                # print(f'{num=} {inj_arg[num][key]=}')
                            else:
                                stopper = 1
                                inj_data = ''
                                data = ''

                        elif isinstance(inj_arg, dict):
                            if key and key in inj_arg:
                                inj_data = inj_arg[key]
                            # elif num + 1 in inj_arg:
                            #     inj_data = inj_arg[num + 1]
                            else:
                                inj_data = 'Not found'

                                # print(f'{inj_arg=} {key=} {num=}')
                        elif isinstance(inj_arg, tuple):
                            print('tuple')
                            inj_data = 'Not found'
                        else:
                            print(f'ATTENTION: unknown type var: ({inj_var=} {type(inj_arg)=})'
                                  f' in ({file if isinstance(file, str) else "injection"})')
                            inj_data = ''
                    elif inj_var[-5:] == '.html' or inj_var[-4:] == '.css':# or inj_var[-3:] == '.js':  # If not variable, then filename
                        inj_data = self._open_file(self.path(inj_var))
                    else:
                        print(f'ATTENTION: unused var: ({inj_var=})'
                              f' in ({file if isinstance(file, str) else "injection"})')
                        # print(f'{data=}')
                        # inj_var = ''
                        inj_data = ''
                        # data = data[:inj_start] + data[inj_end + 2:]
                        data = ''
                    if layer <= DEEPNESS:
                        inj_data, _ = self._just_inject_in_that_file(inj_data, file, num)
                    data = data[:inj_start] + inj_data + data[inj_end + 2:]
                    # print(f'{data =}')
                    # print(f'{inj_var=} {inj_file=}')
                else:
                    layer += 1
                    # print(f'LAYER: {layer}')

        except Exception as e:
            self.error += 1
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f'{fname}[{exc_tb.tb_lineno}]ERROR: while parsing view: ({file}) {e} error#{self.error}')
            if self.error >= 1:
                sys.exit(1)
            return '500'
        # print(f'====DATA: {data}')
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

    def _try_parse_cycle(self, inj_var, inj_start, inj_end, data, file):
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
            inj_end = cycle_end + 5
            data = f'{data[:inj_start]}{cycles_data}{data[inj_end:]}'
            # print(f'CYCLES ENDED: {data=}')
            return True, data, inj_end
        return False, data, inj_end

    def _try_parse_condition(self, inj_var, inj_start, inj_end, data, file):
        condition_pos = inj_var.find('?')
        if condition_pos >= 0:
            condition_not_met = False
            condition_end = data.find('{{?}}', inj_end)
            _inj_end = condition_end + 5

            condition_else = data.find('{{else}}', inj_end, condition_end)
            if condition_else >= 0:
                condition_data_1 = data[inj_end + 2:condition_else]
                condition_data_2 = data[condition_else + 8: condition_end]
            else:
                condition_data_1 = data[inj_end + 2:condition_end]

            operand_1 = inj_var[:condition_pos]
            operand_2 = inj_var[condition_pos + 2:]
            condition = inj_var[condition_pos + 1: condition_pos + 2:]

            # print(f'???? Found condition: ({operand_1} {condition} {operand_2}) in page: {file}')
            o_1 = self._get_value_from_injections(operand_1)
            if condition == '':
                if not o_1:
                    condition_not_met = True
            else:
                o_2 = self._get_value_from_injections(operand_2)
                if o_1 is None or o_2 is None:
                    condition_not_met = True
                elif condition == '=':
                    if o_1 != o_2:
                        condition_not_met = True
                elif condition == '<':
                    if o_1 >= o_2:
                        condition_not_met = True
                elif condition == '>':
                    if o_1 <= o_2:
                        condition_not_met = True
            # print(f'{data=}')
            if condition_not_met:
                # print(f'Condition not met')
                if condition_else == -1:
                    data_without_condition = f'{data[:inj_start]}{data[_inj_end:]}'
                    # Condition is one and not met - cutting condition
                    return True, data_without_condition, inj_start
                # print(f'Condition 2 met')
                condition_data, _ = self._just_inject_in_that_file(condition_data_2, file)
            else:
                # print(f'Condition 1 met')
                condition_data, _ = self._just_inject_in_that_file(condition_data_1, file)
            # print(f'Condition: {condition_data}')
            # print(f'CDATA: {data[:inj_start]}|||{condition_data}|||{data[_inj_end:]}')
            data = f'{data[:inj_start]}{condition_data}{data[_inj_end:]}'
            # Condition 1 or 2 (if present)
            return True, data, inj_start + len(condition_data)
        # No condition found
        return False, data, inj_end

    def _try_parse_dict(self, inj_var):
        dot_pos = inj_var.find(':')
        if dot_pos >= 0:
            obj = inj_var[:dot_pos]
            key = inj_var[dot_pos + 1:]
            # print(f'{key=} {obj=}')
            inj_arg = self._get_value_from_injections(obj)
            # print(f'{type(inj_arg)=}')
            # if isinstance(inj_arg, classmethod):
            #     print(f'{inj_arg.__getattribute__(key)=}')
            #     return inj_arg.__getattribute__(key), key
            # if inj_arg is None:
            #     inj_arg = 'N/A'
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
        return None, 0

    # def _parse_list(self, data):
    #     for i, e in enumerate(data):
    #         # print(f'cycle start: {i}  id:{cycle_dig + i}')
    #         cd, stopper = self._just_inject_in_that_file(cycle_data, file, cycle_dig + i)
    #         if stopper:
    #             break
    #         cycles_data += cd
    #         # print(f'cycle end: {i} {cycle_data=}')
    #     inj_end = cycle_end + 5
    #     data = f'{data[:inj_start]}{cycles_data}{data[inj_end:]}'
    #     # print(f'CYCLES ENDED: {data=}')
    #     return True, data, inj_end

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
        if key in self.frontend_vars.keys():
            return self.frontend_vars[key]
        return None

    def _open_file(self, path):
        with open(path, 'r') as file:
            data = file.read().replace('\n', '').replace('    ', ' ')
            data = self._remove_comments(data, path)
            return data

    def path(self, file_name: str):
        return f'{FRONTEND_PATH}{file_name}'


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
