from time import time


def get_time(req, ans, start_response):
    delta_time = time()
    # Everything is happening here:
    response = ans(start_response, req)
    # Not here:
    delta_time = time() - delta_time
    print(f'Время обработки запроса: {delta_time.__round__(6)}')
    return response