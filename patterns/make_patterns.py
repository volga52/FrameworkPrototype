import abc
import copy
from datetime import datetime
# import json
import os
import jsonpickle

from patterns.unit_of_work import DomainObject


# абстрактный пользователь
class User:
    def __init__(self, name):
        self.id = 0
        self.name = name
        self.account = 'anonymous'
        self.status = 'on'


# Администратор
class Admin(User):
    pass


# зарегистрированный пользователь
class Client(User, DomainObject):
    def __init__(self, name):
        # self.account = ''
        # self.password = ''
        super().__init__(name)
        self.locations = []


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    # auto_id = 0
    types = {
        'admin': Admin,
        'client': Client,
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_='client', name='anonymous'):
        new_elem = cls.types[type_](name)
        # UserFactory.auto_id += 1
        return new_elem


# порождающий паттерн Прототип - Местоположение
class UsersTourPrototype:
    # прототип товара - location

    def clone(self):
        return copy.deepcopy(self)


# Конечный выбираемый объект
class UsersTour(UsersTourPrototype):

    def __init__(self, name, direction):
        self.name = name
        self.direction = direction
        self.direction.locations.append(self)


class Location(DomainObject):

    def __init__(self, id_product, name, direction, price, status):
        self.id_product = id_product
        self.name = name
        # type => int   direction.id
        self.direction = direction
        # 1 - активно 0 - не активно
        self.price = price
        self.status = status

    def __repr__(self):
        return f'class Location {self.id_product} {self.name} {self.direction} ' \
               f'{self.price} {self.status}'


# порождающий паттерн Абстрактная фабрика - фабрика товаров
class LocationFactory:
    '''
    Класс функционала для взаимодействия с сохраненными данными
    '''
    auto_id = 1

    # @staticmethod
    # def generate(name):
    #     return

    # подаем список элементов обекта для класса Location
    # Если товар с таким именем есть выход
    @staticmethod
    def create(data_list):
        '''
        Функция обработки данных для создания нового
        объекта-товара. Запись его в файл.
        Возвращает новый объект
        '''
        # list_sample = ID, [NAME, DIRECTION, PRICE], STATUS
        if LocationFactory.check_name(data_list[0]):
            print('Элемент с таким именем уже есть')
            return
        # Ставим id
        list_work = [LocationFactory.auto_id]
        # Вставляем пришедшие данные
        list_work.extend(data_list)
        # Ставим status: 1
        list_work.append(1)

        new_obj = Location(*list_work)
        # dict_new_class = vars(new_class)
        LocationFactory.add_to_file(new_obj)

        return new_obj

    @staticmethod
    def get_location(data_list):
        # list_sample = [ID, NAME, DIRECTION, PRICE, STATUS]
        return Location(*data_list)

    @staticmethod
    def add_to_file(product):
        '''
        Функция добавляет товар в файл
        получает Python-список объектов
        '''
        if product:
            with open("data_file_00.json", 'r', encoding='utf-8') as r_f:
                load_data = r_f.read()
                json_list_ = jsonpickle.loads(load_data)
                json_list_.append(product)

            LocationFactory.save_file(json_list_)

            # with open("data_file_00.json", 'w', encoding='utf-8') as w_f:
            #     save_data = jsonpickle.dumps(json_list_)
            #     w_f.write(save_data)

    @staticmethod
    def check_name(products_name):
        '''
        Функция проверяет имя на повтор
        в файле. Получает имя объекта
        Возвращает true или false
        Меняет auto_id в Location
        '''
        all_products = LocationFactory.load_all_from_file()

        if len(all_products) > 0:
            # Учетчик id элементов
            list_id = []
            for i in all_products:
                list_id.append(int(i.id_product))
                if i.name == products_name:
                    return True
            LocationFactory.auto_id = max(list_id) + 1
        return False

    @staticmethod
    def load_all_from_file():
        '''
        Функция считывает из JSON файла данные
        Возвращает список объектов товаров
        '''
        with open("data_file_00.json", 'r', encoding='utf-8') as r_f:
            goods_list = r_f.read()
            goods_list = jsonpickle.loads(goods_list)
        return goods_list

    @staticmethod
    def delete_to_file(product):
        '''Функция удаляет элемент из "базы": файла'''
        goods_list = LocationFactory.load_all_from_file()
        for i in goods_list:
            if i.id_product == product.id_product:
                goods_list.remove(product)
                LocationFactory.save_file(goods_list)
                return
        print('Такого товара нет в файле')

    @staticmethod
    def clear_all():
        pass

    @staticmethod
    def save_file(goods_list):
        '''Функция записывает файл с данными'''
        with open("data_file_00.json", 'w', encoding='utf-8') as w_f:
            save_data = jsonpickle.dumps(goods_list)
            w_f.write(save_data)


# Тип 'по дням'
class ByDaysLocation(Location):
    pass


# Тип 'путевка'
class PackageLocation(Location):
    pass


# Направление - категория
class Direction(DomainObject):
    auto_id = 0

    def __init__(self, public_name):
        self.public_name = public_name
        self.locations = []
        Direction.auto_id += 1
        self.id = Direction.auto_id

    def location_count(self):
        return sum([len(i) for i in self.locations])

    # Поиск 'направления по' id или public_name
    @staticmethod
    def find_direction_by_param(list_directions, param):
        if type(param) == int:
            for item in list_directions:
                if item.id == param:
                    # print('item', item.id)
                    return item
        elif type(param) == str:
            for item in list_directions:
                if item.public_name == param:
                    # print('item', item.name_public)
                    return item
        # raise Exception(f'Нет направления с id = {id}')
        return False


# порождающий паттерн Абстрактная фабрика - фабрика курсов
class UserTourFactory:
    types = {
        'package': PackageLocation,
        'bydays': ByDaysLocation,
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, direction):
        return cls.types[type_](name, direction)


# Основной интерфейс
# class Engine:
#     def __init__(self):
#         self.directions = None
#         self.get_directions_default()
#         self.users = []
#
#         self.catalog = Catalog(self.directions)
#         self.cart = None
#
#         self.init_basket()
#
#     def get_location(self, name):
#         for item in self.catalog.goods_list:
#             if item.name == name:
#                 return item
#         return None
#
#     @staticmethod
#     def decode_value(val):
#         val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
#         val_decode_str = quopri.decodestring(val_b)
#         return val_decode_str.decode('UTF-8')
#
#     # Получение списка имен Направлений
#     def get_list_directions_names(self):
#         return [elem.public_name for elem in self.directions]
#
#     # Загрузка основных направлений
#     def get_directions_default(self):
#         default_direction_list = [
#             'Прибалтика',
#             'Южное направление',
#             'Дальний Восток',
#             'Центральная Россия',
#             'Север',
#             'Экстрим',
#         ]
#
#         self.directions = [Direction(i) for i in default_direction_list]
#
#     # Поиск 'направления по' id или public_name
#     @staticmethod
#     def find_direction_by_param(list_directions, param):
#         if type(param) == int:
#             for item in list_directions:
#                 if item.id == param:
#                     # print('item', item.id)
#                     return item
#         elif type(param) == str:
#             for item in list_directions:
#                 if item.public_name == param:
#                     # print('item', item.name_public)
#                     return item
#         # raise Exception(f'Нет направления с id = {id}')
#         return False
#
#     def init_user(self):
#         new_user = UserFactory.create()
#         self.users.append(new_user)
#         return new_user
#
#     def init_basket(self):
#         self.cart = Basket(self.directions, self.init_user())


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name
        self.text = None

    def log(self, text):
        date_now = datetime.now()
        self.text = f'{date_now} {text}'
        self.save_to_file()
        print('log--->', text)

    def save_to_file(self):
        path = os.getcwd()
        file_name = f"{path}\\logs\\{self.name}_log.log"

        with open(file_name, 'a+', encoding='utf-8') as file:
            file.write(self.text)


# if __name__ == '__main__':
    # catalog = Catalog()
    #
    # LocationFactory.create(['first', 1, 100])
    # LocationFactory.create(['second', 1, 100])
    # LocationFactory.create(['два', 2, 150])
    # LocationFactory.create(['три', 2, 150])
    # LocationFactory.delete_to_file({"id_product": 1, "name": "first", "direction": 1, "status": 1, "price": 100})
    # LocationFactory.create(['sixth', 3, 100])
    # print(catalog)
