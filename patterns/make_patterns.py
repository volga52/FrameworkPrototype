import abc
import copy
import json
import quopri


# абстрактный пользователь
class User:
    pass


# администратор
class Admin(User):
    pass


# зарегистрированный пользователь
class LegalUser(User):
    pass


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'admin': Admin,
        'legal_user': LegalUser,
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


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


class Location:

    def __init__(self, id_product, name, direction, price, status):
        self.id_product = id_product
        self.name = name
        # type => int   direction.id
        self.direction = direction
        self.name_direction = None
        # 1 - активно 0 - не активно
        self.status = status
        self.price = price

    def __repr__(self):
        return f'class Location {self.id_product} {self.name} {self.direction} ' \
               f'{self.name_direction} {self.price} {self.status}'


class KitElem(metaclass=abc.ABCMeta):
    def __init__(self):
        # Список объектов
        self.goods_list = []
        self.cost = None
        self.directions = []
        # Список словарей (проверенный)
        self.list_for_html = []

        self.get_directions()

        self.init_interface()

    def __repr__(self):
        return f'Это весь лист {self.list_for_html}'

    @abc.abstractmethod
    def get_directions(self):
        pass

    def init_interface(self):
        # Получение списка товаров
        list_products = self.get_list_products()
        if list_products:
            # Обработка листа товаров для заполнения аргументов класса
            for _dict in list_products:
                # Новый класс Товара
                new_location = Location(**_dict)
                # Добавление в список
                self.goods_list.append(new_location)
                # Определяем обновляемое Направление по id
                direction_record = self.find_direction_by_id(new_location.direction)
                # Записываем название направления в новый продукт
                new_location.name_direction = direction_record.public_name
                # Записываем id продукта в список-продуктов направления
                direction_record.locations.append(new_location.id_product)

            self.form_list_dicts()

    # Получение списка товаров для обработки
    @abc.abstractmethod
    def get_list_products(self):
        pass

    # Добавить товар в список товаров
    def add_product(self, product):
        if self.check_presence(product):
            self.goods_list.append(product)

    # Удалить товар из списка товаров
    def delete_product(self, product):
        for elem in self.goods_list:
            if elem.id_product == product.id_product:
                index_del_elem = self.goods_list.index(elem)
                self.goods_list.remove(index_del_elem)

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

    # Получение списка словарей для html
    def form_list_dicts(self):
        self.list_for_html = [vars(_class) for _class in self.goods_list]

    # Поиск 'направления по id'
    def find_direction_by_id(self, id):
        for item in self.directions:
            if item.id == id:
                print('item', item.id)
                return item
        raise Exception(f'Нет направления с id = {id}')

    # Получение списка имен Направлений
    def get_list_direction(self):
        return [elem.public_name for elem in self.directions]


class Catalog(KitElem):
    # Загрузка основных напрвлений
    def get_directions(self):
        default_direction_list = [
            'Прибалтика',
            'Южное направление',
            'Дальний Восток',
            'Центральная Россия',
            'Север',
            'Экстрим',
        ]
        for i in default_direction_list:
            new_direction = Direction(i)
            self.directions.append(new_direction)

    # Собственный метод Catalog
    def get_list_products(self):
        return LocationFactory.load_all_from_file()


class Basket(KitElem):
    def __init__(self, list_directions, list_):
        super().__init__()
        self.list_directions = list_directions
        self._list = list_

    def get_directions(self):
        list_directions = [elem.public_name for elem in self.list_directions]
        for i in list_directions:
            new_direction = Direction(i)
            self.directions.append(new_direction)

    def get_list_products(self):
        # Должен вернуть список словарей
        return


# порождающий паттерн Абстрактная фабрика - фабрика товаров
class LocationFactory:
    auto_id = 1

    # подаем список элементов обекта для класса Location
    # Если товар с таким именем есть выход
    @staticmethod
    def create(data_list):
        # list_sample = ID, [NAME, DIRECTION, PRICE], STATUS
        if LocationFactory.check_name(data_list[0]):
            print('Элемент с таким именем уже есть')
            return
        # Ставим id
        list_work = [LocationFactory.auto_id]
        # Вставляем пришедшие данные
        list_work.extend(data_list)
        # Ставим
        list_work.append(1)

        new_class = Location(*list_work)
        dict_new_class = vars(new_class)
        LocationFactory.add_to_file(dict_new_class)

        return new_class

    @staticmethod
    def add_to_file(product):
        '''
        Функция добавляет товар в файл
        получает Python-объект словарь
        '''
        if product:
            with open("data_file.json", 'r', encoding='utf-8') as r_f:
                json_list = json.load(r_f)
                json_list.append(product)

            with open("data_file.json", 'w', encoding='utf-8') as w_f:
                json.dump(json_list, w_f, ensure_ascii=False)

    @staticmethod
    def check_name(products_name):
        '''
        Функция проверяет имя на повтор
        в файле получает имя объекта
        '''
        all_products = LocationFactory.load_all_from_file()
        if len(all_products) > 0:
            list_id = []
            for i in all_products:
                list_id.append(int(i['id_product']))
                if i['name'] == products_name:
                    return True
            LocationFactory.auto_id = max(list_id) + 1
        return False

    @staticmethod
    def load_all_from_file():
        '''
        Функция считывает из JSON файла данные
        Возвращает список словарей
        '''
        # goods_list = []
        with open("data_file.json", 'r', encoding='utf-8') as r_f:
            goods_list = json.load(r_f)
        return goods_list

    @staticmethod
    def delete_to_file(product):
        '''Функция удаляет элемент из "базы", файла'''
        goods_list = LocationFactory.load_all_from_file()
        for i in goods_list:
            if i['id_product'] == product['id_product']:
                goods_list.remove(product)
                LocationFactory.save_file(goods_list)
                return
        print('Такого товара нет в файле')

    @staticmethod
    def clear_all():
        pass

    @staticmethod
    def save_file(goods_list):
        with open("data_file.json", 'w', encoding='utf-8') as w_f:
            json.dump(goods_list, w_f, indent=4, ensure_ascii=False)


# Тип 'путевка'
class PackageLocation(Location):
    pass


# Тип 'по дням'
class ByDaysLocation(Location):
    pass


# Направление - категория
class Direction:
    auto_id = 0

    def __init__(self, public_name):
        self.public_name = public_name
        self.locations = []
        Direction.auto_id += 1
        self.id = Direction.auto_id

    def location_count(self):
        return sum([len(i) for i in self.locations])


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
class Engine:
    def __init__(self):
        self.class_ap = []

        # self.default_direction()
        self.catalog = Catalog()

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_user_tour(type_, name, direction):
        return UserTourFactory.create(type_, name, direction)

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

    @staticmethod
    def log(text):
        print('log--->', text)


if __name__ == '__main__':
    catalog = Catalog()

    LocationFactory.create(['first', 1, 100])
    LocationFactory.create(['second', 1, 100])
    LocationFactory.create(['два', 2, 150])
    LocationFactory.create(['три', 2, 150])
    # LocationFactory.delete_to_file({"id_product": 1, "name": "first", "direction": 1, "status": 1, "price": 100})
    print(catalog)
