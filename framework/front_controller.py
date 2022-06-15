import setup
from time import time


class Middleware:
    def __init__(self):
        self.setup = setup.MIDDLEWARE_SETUP
        self.delta_time = None
        if 'cors_ip_whitelist' in self.setup.keys():
            self.cors_ip_whitelist = self.setup['cors_ip_whitelist']
        if 'cors_ip_blacklist' in self.setup.keys():
            self.cors_ip_blacklist = self.setup['cors_ip_blacklist']
        # print(f'{self.setup=} {self.cors_ip_whitelist=}')

    def answer_time(self, request, response, responser, start: bool):
        if start:
            self.delta_time = time()
        else:
            self.delta_time = time() - self.delta_time
            print(f'Время обработки запроса "{request.path}": '
                  f'{self.delta_time.__round__(4) if self.delta_time > 0.0001 else 0}')
        return response

    def cors(self, request, response, responser, start: bool):
        if start:
            # print(f'{self.cors_ip_whitelist=} {request.client_ip4=}')
            if self.cors_ip_whitelist and request.client_ip4 not in self.cors_ip_whitelist:
                responser.status_404()
                print(f'Попытка доступа не из белого списка <{request.client_ip4}>, ответ: {responser.status}')
            elif self.cors_ip_blacklist and request.client_ip4 in self.cors_ip_blacklist:
                responser.status_404()
                print(f'Попытка доступа из черного списка <{request.client_ip4}>, ответ: {responser.status}')
        return response
