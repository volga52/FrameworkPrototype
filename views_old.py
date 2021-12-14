from framework.templator import render

from patterns.make_patterns import Logger, Engine, Direction

site = Engine()
logger = Logger('main')


class Index:
    def __call__(self, request):
        # Добаавляем request 'list_locations'
        def selection(id_, request_):
            '''
            Функция делает выборку по направлению
            и заносит полученный список в request
            для вывода на странице
            '''
            list_ = [elem for elem in site.catalog.list_for_html if elem['direction'] == int(id_)]
            request_['catalog'] = list_

        # Список функций обработчиков
        functions_dict = {
            'id_direction': selection,
        }

        request['catalog'] = site.catalog.list_for_html

        # Преобразуем объект класса в список словарей
        directions_list = [vars(i) for i in site.catalog.directions]
        # Словарь, содержащий данные (словари) из GET-запроса
        get_dict = request.get('data_get')
        # Запуск обработчиков словарей GET-запросов
        if get_dict:
            for key in get_dict.keys():
                functions_dict[key](get_dict.get(key), request)
        # print(request)
        return '200 OK', render('index.html', context=request,
                                directions=directions_list)


class Basket:
    def __call__(self, request):
        request['cart'] = site.cart.list_for_html

        # Преобразуем объект класса в список словарей
        directions_list = [vars(i) for i in site.catalog.directions]

        return '200 OK', render('basket.html', context=request, directions=directions_list)


class History:
    def __call__(self, request):
        return '200 OK', render('history.html', context=request)


class Admin:
    def __call__(self, request):

        def create_new_direction(name_direction):
            '''Создание новой директории'''
            # Требуется валидация имени
            if len(name_direction) > 1:
                site.catalog.directions.append(Direction(name_direction))
            else:
                print('Имя не соответствует требованиям')

        def delete_direction(name_direction):
            '''Функция удаляет деректорию-направление'''
            for elem in site.catalog.directions:
                if elem.public_name == name_direction:
                    site.catalog.directions.remove(elem)
                else:
                    print('Такого элемента не существует')

        def new_location(data_list):
            '''
            Функция создаёт новый товар
            Принимает список-кортеж элементов
            NAME, DIRECTION, PRICE (если нет, то 0)
            '''
            elem_index_1 = site.catalog.find_direction_by_param(data_list[1])
            # Формирование DIRECTION. Требуется id из списка
            if elem_index_1:
                print(f'Это id direction: {elem_index_1.id}')
                elem_index_1 = elem_index_1.id
            else:
                print(f'Нет направления с id = {elem_index_1}')
                return

            elem_index_2 = int(data_list[2]) if type(data_list[2]) == int else 0
            data_list = (data_list[0], elem_index_1, elem_index_2)

            if input(f'Отправить data_list, для создания нового объекта?') == 'Yes':
                message = site.catalog.add_product(data_list)
                request['message'] = message

        # Словарь обработки
        functions_dict = {
            'new_direction': create_new_direction,
            'delete_direction': delete_direction,
            'new_location': new_location,
        }

        # Словарь данные POST-запроса
        post_dict = request.get('data_post')
        # Обработчик данных POST-запроса по словарю
        if post_dict:
            for key in post_dict.keys():
                if key in functions_dict:
                    functions_dict[key](post_dict.get(key))

        request['list_directions'] = site.catalog.get_list_directions_names()
        return '200 OK', render('admin.html', context=request)


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'
