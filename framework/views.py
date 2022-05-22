
class View:
    def __init__(self, frontend_path: str = 'frontend', frontend_vars: dict = None):
        self.frontend_path = frontend_path
        self.frontend_vars = frontend_vars

    def view(self, page_name: str = 'index.html'):
        with open(f'{self.frontend_path}{page_name}', 'r') as file:
            data = file.read().replace('\n', '').replace('    ', ' ')
        # Заменяем переменные на код из внешних файлов
        data = self._just_include_that_file(data)
        # Заменяем переменные на ссылки пользователя
        for var, link in self.frontend_vars.items():
            data = data.replace(var, link)
        return data

    # Костыли. Нагугленные способы импорта на сервере не работают
    def _just_include_that_file(self, data):
        while True:
            include_start = data.find('{{')
            if include_start >= 0:
                include_end = data.find('}}', include_start) + 2
                include_file = data[include_start + 2: include_end - 2]
                with open(f'{self.frontend_path}{include_file}', 'r') as file:
                    include_data = file.read().replace('\n', '').replace('    ', ' ')
                data = data[:include_start] + include_data + data[include_end:]
                # print(f'{data =}')
                # print(f'{include_data =}')
            else:
                break
        return data

        # def __init__(self,
        #              page_path: str = 'frontend/',
        #              page_name: str = 'index'):
        #     self.page_path = page_path
        #     self.page_name = page_name
        #
        # def set_page(self):
        #     with open(f'{self.page_path}{self.page_name}.html', 'r') as file:
        #         data = file.read().replace('\n', '')
        #     return data
