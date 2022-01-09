from framework.templator import render
from patterns.behavioral_patterns import Subject

from patterns.make_patterns import Logger, Direction, UserFactory, Location
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, BaseSerializer
from patterns.mappers import MapperRegistry
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import ListView, CreateView
from patterns.unit_of_work import UnitOfWork
from patterns.engine import Engine

UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

site = Engine()
logger = Logger('main')

# Элемент для варианта с Декораторами
routes = {}


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
            list_ = Direction.find_direction_by_param(
                site.directions, int(id_)).locations
            request_['catalog'] = list_

        def add_to_cart(id_, request_):
            '''
            Функция добавляет элемент по id в корзину
            '''
            id_ = int(id_)
            add_elem = None
            for elem in site.catalog.goods_list:
                if elem.id_product == id_:
                    add_elem = elem
            site.cart.goods_list.append(add_elem)

        # Список функций обработчиков
        functions_dict = {
            'id_direction': selection,
            'add_to_cart': add_to_cart,
        }

        # Список товаров
        request['catalog'] = site.catalog.goods_list

        # Список директорий
        directions_list = site.directions
        # Словарь, содержащий данные (словари) из GET-запроса
        get_dict = request.get('data_get')
        # Запуск обработчиков словарей GET-запросов
        if get_dict:
            for key in get_dict.keys():
                functions_dict[key](get_dict.get(key), request)
        return '200 OK', render('index.html', context=request,
                                directions=directions_list)


@AppRoute(routes=routes, url='/basket/')
class Basket:
    @Debug(name='Basket', logger=logger)
    def __call__(self, request):
        request['cart'] = site.cart.goods_list

        directions_list = site.directions

        return '200 OK', render('basket.html', context=request,
                                directions=directions_list)


@AppRoute(routes=routes, url='/history/')
class History:
    @Debug(name='History', logger=logger)
    def __call__(self, request):
        return '200 OK', render('history.html', context=request)


@AppRoute(routes=routes, url='/admin/')
class Admin:
    @Debug(name='Admin', logger=logger)
    def __call__(self, request):

        # Класс функций обработки событий
        workplace = WorkplaceAdmin(site, request)

        # Словарь обработки
        functions_dict = {
            'new_direction': workplace.create_new_direction,
            'delete_direction': workplace.delete_direction,
            'new_location': workplace.new_location,
            'delete_loc': workplace.delete_location,
        }

        # Словарь - данные POST-запроса
        post_dict = request.get('data_post')
        # Обработчик данных POST-запроса по словарю
        if post_dict:
            for key in post_dict.keys():
                if key in functions_dict:
                    functions_dict[key](post_dict.get(key))
            workplace.notify()

        request['list_directions'] = site.get_list_directions_names()
        request['list_goods'] = site.catalog.get_list_goods_names()
        return '200 OK', render('admin.html', context=request)


@AppRoute(routes=routes, url='/load_all/')
class AllProducts:
    @Debug(name='AllProducts', logger=logger)
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.catalog.goods_list).save()


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# Страница 'Список клиентов'
@AppRoute(routes=routes, url='/client-list/')
class ClientListView(ListView):
    # queryset = site.users
    template_name = 'client-list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('client')
        return set(site.users).union(set(mapper.all()))


@AppRoute(routes=routes, url='/location-list/')
class LocationListView(ListView):
    queryset = site.catalog.goods_list
    template_name = 'location-list.html'


@AppRoute(routes=routes, url='/create-user/')
class UserCreateView(CreateView):
    template_name = 'create-user.html'

    def create_obj(self, data: dict):
        name = data['new_user_name']
        specs = data['new_user_specs']
        name = site.decode_value(name)

        new_object = UserFactory.create(specs, name)
        site.users.append(new_object)

        new_object.mark_new()
        UnitOfWork.get_current().commit()


class WorkplaceAdmin(Subject):
    def __init__(self, site, request):
        self.site = site
        self.request = request
        super().__init__()

    def create_new_direction(self, name_direction):
        '''Создание новой директории'''
        # Требуется валидация имени
        if len(name_direction) > 1:
            new_object = Direction(name_direction)
            self.site.directions.append(new_object)

            new_object.mark_new()
            UnitOfWork.get_current().commit()
        else:
            print('Имя не соответствует требованиям')

    def delete_direction(self, name_direction):
        '''Функция удаляет деректорию-направление'''
        for elem in self.site.directions:
            if elem.public_name == name_direction:
                self.site.directions.remove(elem)

                elem.mark_removed()
                UnitOfWork.get_current().commit()
                return
        print('Такого элемента не существует')
        return

    def new_location(self, data_list):
        '''
        Функция создаёт новый товар
        Принимает список-кортеж элементов
        NAME, DIRECTION, PRICE (если нет, то 0)
        '''
        # Построение параметров для создания Location
        # Формирование DIRECTION.
        elem_index_1 = Direction.find_direction_by_param(self.site.directions, data_list[1])
        # Требуется id из списка. Проверка
        if elem_index_1:
            # print(f'Это id direction: {elem_index_1.id}')
            elem_index_1 = elem_index_1.id
        else:
            print(f'Нет направления с id = {elem_index_1}')
            return
        # формирование Price стоимость введенная, если ошибка - 0
        elem_index_2 = int(data_list[2]) if type(data_list[2]) == int else 0
        # Итоговый кортеж данных. id = 0 Последний элемент Status = 1
        data_list = (0, data_list[0], elem_index_1, elem_index_2, 1)

        if input(f"Создать новый объект из данных {data_list}? Да - Y ") == 'Y':
            new_obj = Location(*data_list)
            try:
                new_obj.mark_new()
                UnitOfWork.get_current().commit()
                # Получаем новый элемент из таблицы
                new_obj = site.catalog.get_location_from_db(new_obj)

                # Обрабатываем в каталоге
                result = self.site.catalog.add_good(new_obj)
                self.request['message_CRUD'] = result[1]
                if result[0]:
                    self.observers.append(email_notifier)
                    self.observers.append(sms_notifier)
            except:
                pass

    def delete_location(self, name):
        del_obj = None
        for elem in self.site.catalog.goods_list:
            if elem.name == name:
                del_obj = elem
                break
        if del_obj:
            if input(f'Удалить элемент {type(del_obj)} Да: Y ') == 'Y':
                try:
                    # Удаляем из БД
                    del_obj.mark_removed()
                    UnitOfWork.get_current().commit()
                    # Удаляем из каталога
                    self.site.catalog.goods_list.remove(del_obj)
                    # Удаляем из списка соответствующей директории
                    search_direction = Direction.find_direction_by_param(self.site.directions, del_obj.direction)
                    search_direction.locations.remove(del_obj)
                    self.request['message_CRUD'] = f'Товар c именем {name} удален'
                except:
                    self.request['message_CRUD'] = 'Что-то пошло не так'
                    raise
            else:
                print('Удаление отменено')
        else:
            print('Товар не найден')
