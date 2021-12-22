import quopri
import sqlite3

from patterns.make_patterns import Catalog, UserFactory, Basket
from patterns.mappers import DirectionMapper


class Engine:
    connection = sqlite3.connect('patterns.sqlite')

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
        mapper = DirectionMapper(self.connection)
        self.directions = mapper.all()

    # # Поиск 'направления по' id или public_name
    # @staticmethod
    # def find_direction_by_param(list_directions, param):
    #     if type(param) == int:
    #         for item in list_directions:
    #             if item.id == param:
    #                 # print('item', item.id)
    #                 return item
    #     elif type(param) == str:
    #         for item in list_directions:
    #             if item.public_name == param:
    #                 # print('item', item.name_public)
    #                 return item
    #     # raise Exception(f'Нет направления с id = {id}')
    #     return False

    def init_user(self):
        new_user = UserFactory.create()
        self.users.append(new_user)
        return new_user

    def init_basket(self):
        self.cart = Basket(self.directions, self.init_user())
