from framework.requests import PostRequestsNew, GetRequests


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:

    """Класс Framework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj
        self.type_request = {'POST': PostRequestsNew, 'GET': GetRequests}

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        path = environ['PATH_INFO']
        print(path)
        # print(environ)

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        # Создаем и наполняем словарь данными из запрос
        request = {}

        method = environ['REQUEST_METHOD']
        # Определяем класс обработки сообщения
        class_request = self.type_request[method]()
        # Получаем переданную информацию
        data = class_request.get_request_params(environ)
        # Заносим информацию в request
        # 'POST' - request['data'], 'GET' - request['request_params']
        request[class_request.request_name_agr] = data

        # Запись источника (для get-запроса)
        # 'navigate' - соответствует запросу информации
        # 'no-cors' - из того же источника или повтор
        fetch_mode = environ['HTTP_SEC_FETCH_MODE']
        request['FETCH_MODE'] = fetch_mode

        print(f'Нам пришёл {method} запрос: {data}, debug fetch_mode: {fetch_mode}')

        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts_lst:
            front(request)
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
