# структурный паттерн - Декоратор
from time import time


class AppRoute:
    '''
    Декоратор для views. Принимает
    Контроллер и
    ссылку для его запуска
    '''
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:
    '''
    Декоратор для вывода отладочной информации
    '''
    def __init__(self, name, logger):
        self.name = name
        self.logger = logger

    def __call__(self, cls):
        # это функция декорирует каждый отдельный метод класса
        def timeit(method):
            '''
            Обертка для каждого метода декорируемого класса
            '''
            def timed(*args, **kw):
                time_start = time()
                result = method(*args, **kw)
                time_end = time()
                delta = time_end - time_start

                result_string = f'debug --> {self.name} выполнялся {delta:2.2f} ms'

                # print(result_string)
                self.logger.log(result_string)

                return result

            return timed

        return timeit(cls)
