def view(page_name: str = 'index.html', link_vars: dict = None):
    with open(f'{page_name}', 'r') as file:
        data = file.read().replace('\n', '')
    for var, link in link_vars.items():
        data = data.replace(var, link)
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
