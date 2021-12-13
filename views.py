from framework.templator import render
from patterns.behavioral_patterns import Subject

from patterns.make_patterns import Logger, Engine, Direction
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, BaseSerializer
from patterns.structural_patterns import AppRoute, Debug

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


# Элемент для варианта с Декораторами
routes = {}


# @AppRoute(routes=routes, url='/index/')
class Index:
    @Debug(name='Index', logger=logger)
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
        # directions_list = [vars(i) for i in site.catalog.directions]
        directions_list = [vars(i) for i in site.directions]
        # Словарь, содержащий данные (словари) из GET-запроса
        get_dict = request.get('data_get')
        # Запуск обработчиков словарей GET-запросов
        if get_dict:
            for key in get_dict.keys():
                functions_dict[key](get_dict.get(key), request)
        # print(request)
        return '200 OK', render('index.html', context=request,
                                directions=directions_list)


@AppRoute(routes=routes, url='/basket/')
class Basket:
    @Debug(name='Basket', logger=logger)
    def __call__(self, request):
        request['cart'] = site.cart.list_for_html

        # Преобразуем объект класса в список словарей
        directions_list = [vars(i) for i in site.directions]

        return '200 OK', render('basket.html', context=request, directions=directions_list)


@AppRoute(routes=routes, url='/history/')
class History:
    @Debug(name='History', logger=logger)
    def __call__(self, request):
        return '200 OK', render('history.html', context=request)


@AppRoute(routes=routes, url='/admin/')
class Admin:
    @Debug(name='Admin', logger=logger)
    def __call__(self, request):

        # Класс функций обработки
        workplace = WorkplaceAdmin(site, request)

        # Словарь обработки
        functions_dict = {
            'new_direction': workplace.create_new_direction,
            'delete_direction': workplace.delete_direction,
            'new_location': workplace.new_location,
        }

        # Словарь данные POST-запроса
        post_dict = request.get('data_post')
        # Обработчик данных POST-запроса по словарю
        if post_dict:
            for key in post_dict.keys():
                if key in functions_dict:
                    functions_dict[key](post_dict.get(key))
            workplace.notify()

        request['list_directions'] = site.get_list_direction()
        return '200 OK', render('admin.html', context=request)


@AppRoute(routes=routes, url='/load_all/')
class AllProducts:
    @Debug(name='AllProducts', logger=logger)
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.catalog.goods_list).save()


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class WorkplaceAdmin(Subject):
    def __init__(self, site, request):
        self.site = site
        self.request = request
        super().__init__()

    def create_new_direction(self, name_direction):
        '''Создание новой директории'''
        # Требуется валидация имени
        if len(name_direction) > 1:
            self.site.directions.append(Direction(name_direction))
        else:
            print('Имя не соответствует требованиям')

    def delete_direction(self, name_direction):
        '''Функция удаляет деректорию-направление'''
        for elem in self.site.directions:
            if elem.public_name == name_direction:
                self.site.directions.remove(elem)
                return
        print('Такого элемента не существует')
        return

    def new_location(self, data_list):
        '''
        Функция создаёт новый товар
        Принимает список-кортеж элементов
        NAME, DIRECTION, PRICE (если нет, то 0)
        '''
        elem_index_1 = self.site.find_direction_by_param(self.site.directions, data_list[1])
        # Формирование DIRECTION. Требуется id из списка
        if elem_index_1:
            print(f'Это id direction: {elem_index_1.id}')
            elem_index_1 = elem_index_1.id
        else:
            print(f'Нет направления с id = {elem_index_1}')
            return

        elem_index_2 = int(data_list[2]) if type(data_list[2]) == int else 0
        data_list = (data_list[0], elem_index_1, elem_index_2)

        if input("Создать новый объект из данных POST? Да - Y ") == 'Y':
            result = self.site.catalog.add_product(data_list)
            self.request['message'] = result[1]
            self.observers.append(email_notifier)
            self.observers.append(sms_notifier)
