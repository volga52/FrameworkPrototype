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

        self.init_params()

    def __repr__(self):
        return f'Это список объектов {jsonpickle.dumps(self.goods_list)}'

    # Получение списка товаров
    @abc.abstractmethod
    def get_list_goods(self):
        pass

    def processing_new_good(self, new_location):
        # Добавление в список
        self.goods_list.append(new_location)
        direction_update = None
        if not hasattr(new_location, 'name_direction'):
            # Определяем обновляемое Направление по id
            direction_update = Direction.find_direction_by_param(self.directions, new_location.direction)
            # Записываем название (name_direction) направления в новый продукт
            new_location.name_direction = direction_update.public_name

        # Заносим продукт в список-продуктов направления
        direction_update.locations.append(new_location)
        return new_location

    def init_params(self):
        list_goods = self.get_list_goods()
        if len(list_goods) > 0:
            for obj in list_goods:
                self.processing_new_good(obj)

    @abc.abstractmethod
    def add_good(self, elem):
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
    # Получение списка товаров
    def get_list_goods(self):
        return DataBaseWorker.get_all_from_table('location')

    def add_good(self, new_loc):
        if not new_loc:
            return False, 'Что-то пошло не так'

        self.processing_new_good(new_loc)
        return True, 'Товар добавлен'

    @staticmethod
    def get_location_from_db(obj):
        return DataBaseWorker.get_location_from_table(obj.name)

    def get_list_goods_names(self):
        return [elem.name for elem in self.goods_list]


class Basket(KitElem):
    def __init__(self, _directions, user):
        super().__init__(_directions)
        self.user = user


    def get_list_goods(self):
        return self.goods_list

    def add_good(self, elem):
        self.goods_list.append(elem)
