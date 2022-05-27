
class View:
    def __init__(self,
                 frontend_path: str = 'frontend',
                 frontend_vars: dict = None,
                 page_template: str = ''):
        self.frontend_path = frontend_path
        self.frontend_vars = frontend_vars
        self.page_template = page_template
        self.page_name = ''

    def view(self, page_name: str = 'index.html'):
        self.page_name = page_name
        with open(f'{self.frontend_path}{self.page_template if self.page_template else self.page_name}', 'r') as file:
            page = file.read().replace('\n', '').replace('    ', ' ')
        # Заменяем переменные на содержимое из внешних файлов
        if self.page_template:
            page = self._just_include_that_file(page)
        data = self._just_include_that_file(page)
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
                include_text = data[include_start + 2: include_end - 2]
                include_file = self.page_name if include_text == 'content' else include_text
                with open(f'{self.frontend_path}{include_file}', 'r') as file:
                    include_data = file.read().replace('\n', '').replace('    ', ' ')
                data = data[:include_start] + include_data + data[include_end:]
                # print(f'{data =}')
                # print(f'{include_data =}')
            else:
                break
        return data
