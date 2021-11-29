import copy


# абстрактный пользователь
import quopri


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
class LocationPrototype:
    # прототип товара

    def clone(self):
        return copy.deepcopy(self)


class Location(LocationPrototype):

    def __init__(self, name, direction):
        self.name = name
        self.direction = direction
        self.direction.locations.append(self)


class PackageLocation(Location):
    pass


class ByDaysLocation(Location):
    pass


# Направление - категория
class Direction:
    auto_id = 0

    def __init__(self, name, direction):
        self.name = name
        self.direction = direction
        self.locations = []
        Direction.auto_id += 1
        self.id = Direction.auto_id

    def location_count(self):
        return sum([len(i) for i in self.locations])


# порождающий паттерн Абстрактная фабрика - фабрика курсов
class LocationFactory:
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
        self.free_seats = 0
        self.locations = []
        self.directions =[]

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_direction(name, direction=None):
        return Direction(name, direction)

    def find_direction_by_id(self, id):
        for item in self.directions:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет направления с id = {id}')

    @staticmethod
    def create_location(type_, name, direction):
        return LocationFactory.create(type_, name, direction)

    def get_location(self, name):
        for item in self.locations:
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
