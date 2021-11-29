from framework.utils import decode_value


class GetRequests:
    def __init__(self):
        self.request_name_agr = 'data'

    @staticmethod
    def parse_input_data(data: str):
        '''
        Функция преобразует пришедшие данные
        вида 'id_elem=1&category=10' в формат словаря
        '''
        result = {}
        if data:
            params = data.split('&')

            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_request_params(environ):
        '''
        Функция получает из GET запроса информацию
        Возвращает словарь с данными
        '''
        # получаем параметры запроса
        query_string = environ['QUERY_STRING']
        # превращаем параметры в словарь
        request_params = GetRequests.parse_input_data(query_string)
        return request_params


class PostRequestsNew(GetRequests):
    def __init__(self):
        super().__init__()
        self.request_name_agr = 'request_params'

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        '''
        Функция получает информацию из запроса
        '''
        # получаем длину тела
        content_length_data = env.get('CONTENT_LENGTH')
        # приводим к int
        content_length = int(content_length_data) if content_length_data else 0
        # считываем данные, если они есть
        # print(f"-{type(env['wsgi.input'])}") -> <class '_io.BufferedReader'>
        # запускаем режим чтения
        # Посмотрите в консоле браузера что грузиться дольше всего - найдете причину!
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        '''
        Функция наполняет словарь декодированными данными из запроса
        '''
        result = {}
        if data:
            # декодируем данные
            data_str = data.decode(encoding='utf-8')
            print(f'строка после декод - {data_str}')
            # собираем их в словарь
            result = self.parse_input_data(data_str)
        return result

    def get_request_params(self, environ):
        '''
        Функция получает из POST запроса информацию
        Возвращает словарь с данными
        '''
        # получаем данные
        data = self.get_wsgi_input_data(environ)
        # превращаем данные в словарь
        data = self.parse_wsgi_input_data(data)
        # обработка 'кирилицы'
        data = decode_value(data)
        return data


# class PostRequests:
#     def __init__(self):
#         self.request_name_agr = 'request_params'
#
#     @staticmethod
#     def parse_input_data(data: str):
#         '''
#         Функция преобразует пришедшие данные
#         вида 'id_elem=1&category=10' в формат словаря
#         '''
#         result = {}
#         if data:
#             params = data.split('&')
#             for item in params:
#                 k, v = item.split('=')
#                 result[k] = v
#         return result
#
#     @staticmethod
#     def get_wsgi_input_data(env) -> bytes:
#         '''
#         Функция получает информацию из запроса
#         '''
#         # получаем длину тела
#         content_length_data = env.get('CONTENT_LENGTH')
#         # приводим к int
#         content_length = int(content_length_data) if content_length_data else 0
#         # считываем данные, если они есть
#         # print(f"-{type(env['wsgi.input'])}") -> <class '_io.BufferedReader'>
#         # запускаем режим чтения
#         # Посмотрите в консоле браузера что грузиться дольше всего - найдете причину!
#         data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
#         return data
#
#     def parse_wsgi_input_data(self, data: bytes) -> dict:
#         '''
#         Функция наполняет словарь декодированными данными из запроса
#         '''
#         result = {}
#         if data:
#             # декодируем данные
#             data_str = data.decode(encoding='utf-8')
#             print(f'строка после декод - {data_str}')
#             # собираем их в словарь
#             result = self.parse_input_data(data_str)
#         return result
#
#     def get_request_params(self, environ):
#         '''
#         Функция получает из POST запроса информацию
#         Возвращает словарь с данными
#         '''
#         # получаем данные
#         data = self.get_wsgi_input_data(environ)
#         # превращаем данные в словарь
#         data = self.parse_wsgi_input_data(data)
#         #
#         data = decode_value(data)
#         return data
