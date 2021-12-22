import abc
import quopri

# from patterns.make_patterns import Catalog, UserFactory, Basket
import jsonpickle

from patterns.make_patterns import UserFactory, Location, Direction, LocationFactory
from patterns.mappers import DataBaseWorker


class Engine:

    def __init__(self):
        self.directions = None
        self.get_directions_default()
        self.users = []

        self.catalog = Catalog(self.directions)
        self.cart = None

        self.init_basket()

    def get_location(self, name):
        for item in self.catalog.goods_list:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')

    # Получение списка имен Направлений
    def get_list_directions_names(self):
        return [elem.public_name for elem in self.directions]

    # Загрузка основных направлений
    def get_directions_default(self):
        # self.directions = DataBaseWorker.get_directions_default()
        self.directions = DataBaseWorker.get_all_from_table('direction')

    def init_user(self):
        new_user = UserFactory.create()
        self.users.append(new_user)
        return new_user

    def init_basket(self):
        self.cart = Basket(self.directions, self.init_user())




class KitElem(metaclass=abc.ABCMeta):
    def __init__(self, _directions):
        # Список объектов
        self.goods_list = []
        self.cost = None
        self.directions = _directions

        self.init_interface()

    def __repr__(self):
        return f'Это список объектов {jsonpickle.dumps(self.goods_list)}'

    def init_interface(self):
        # Получение списка товаров
        list_products = self.get_list_products()
        if len(list_products) > 0:
            # Обработка листа товаров для заполнения аргументов класса
            for obj in list_products:
                # Новый класс Товара
                new_location = Location(**vars(obj))
                self.processing_new_dict(new_location)

    # def get_list_products_start(self):
    #     DataBaseWorker.get_all_from_table()

    # Получение списка товаров (словарей) для обработки
    @abc.abstractmethod
    def get_list_products(self):
        pass

    # Функция получает новый товар - class Location
    # дополняет его Направлением, заносит товар в Направление
    def processing_new_dict(self, new_location):
        # Добавление в список
        self.goods_list.append(new_location)
        # Определяем обновляемое Направление по id
        direction_update = Direction.find_direction_by_param(self.directions, new_location.direction)
        # Записываем название направления в новый продукт
        new_location.name_direction = direction_update.public_name
        # Записываем id продукта в список-продуктов направления
        direction_update.locations.append(new_location.id_product)
        return new_location

    # Добавить товар в список товаров
    @abc.abstractmethod
    def add_product(self, elem):
        pass

    # Удалить товар из списка товаров
    def delete_product(self, product):
        for elem in self.goods_list:
            if elem.id_product == product.id_product:
                self.goods_list.remove(elem)
                return

    # Поиск элементов с указанным Направлением
    def find_to_direction(self, direction):
        return [elem for elem in self.goods_list if elem.direction == direction]

    def clear_all(self):
        self.goods_list = []

    # Проверка есть ли товар в списке
    def check_presence(self, product):
        for elem in self.goods_list:
            if elem.id_product == product.id_product:
                print('Элемент с таким id уже есть')
                return True
        return False


class Catalog(KitElem):
    # Получение списка (словарей) товаров для обработки
    def get_list_products(self):
        return LocationFactory.load_all_from_file()

    # Приходит [NAME, DIRECTION (int), PRICE]
    def add_product(self, data_list):
        new_product = LocationFactory.create(data_list)
        if not new_product:
            return False, 'Что-то пошло не так'

        new_location = self.processing_new_dict(new_product)
        return True, 'Товар добавлен'


class Basket(KitElem):
    def __init__(self, _directions, user):
        super().__init__(_directions)
        self.user = user

    # Получение списка (словарей) товаров для обработки
    def get_list_products(self):
        return self.goods_list

    def add_product(self, data_list):
        self.goods_list.append(data_list)