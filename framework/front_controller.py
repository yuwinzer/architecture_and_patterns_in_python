from time import time


def get_time(request, answer, start_response):
    delta_time = time()
    # Everything is happening here:
    response = answer(start_response, request)
    # Not here:
    delta_time = time() - delta_time
    print(f'Время обработки запроса "{request.path}": {delta_time.__round__(6)}')
    return response
