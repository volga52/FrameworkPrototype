'''
architectural_system_pattern unit of mappers
'''
import sqlite3
from patterns.make_patterns import Client, Direction, Location


class ClientMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'users'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            # id, name, account, status = item
            client = ClientMapper.create_user(item)
            # client.id = id
            # client.account = account
            # client.status = status
            result.append(client)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name, account, status FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return ClientMapper.create_user(result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def find_by_name(self, name):
        statement = f"SELECT id, name, account, status FROM {self.tablename} WHERE name=?"
        self.cursor.execute(statement, (name,))
        result = self.cursor.fetchone()
        if result:
            return ClientMapper.create_user(result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, account, status) VALUES (?, ?, ?)"
        self.cursor.execute(statement, (obj.name, obj.account, obj.status))
        try:
            self.connection.commit()
        except Exception as err:
            raise DbCommitException(err.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as err:
            raise DbUpdateException(err.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)

    @staticmethod
    def create_user(param):
        id, name, account, status = param
        new_client = Client(name)
        new_client.id = id
        new_client.account = account
        new_client.status = status
        return new_client


class DirectionMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'direction'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            obj = DirectionMapper.create_direction(item)
            # id, name = item
            # obj = Direction(name)
            # obj.id = id
            result.append(obj)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, public_name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            # id, public_name = result
            # new_direction = Direction(public_name)
            # new_direction.id = id
            return DirectionMapper.create_direction(result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def find_by_name(self, name):
        statement = f"SELECT id, public_name FROM {self.tablename} WHERE name=?"
        self.cursor.execute(statement, (name,))
        result = self.cursor.fetchone()
        if result:
            return Client(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (public_name) VALUES (?)"
        self.cursor.execute(statement, (obj.public_name,))
        try:
            self.connection.commit()
        except Exception as err:
            raise DbCommitException(err.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET public_name=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        self.cursor.execute(statement, (obj.public_name, obj.id))
        try:
            self.connection.commit()
        except Exception as err:
            raise DbUpdateException(err.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as err:
            raise DbDeleteException(err.args)

    @staticmethod
    def create_direction(param):
        id, name = param
        new_direction = Direction(name)
        new_direction.id = id
        return new_direction


class LocationMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'users'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            location = Location(*item)
            result.append(location)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id_product, name, direction, price, status FROM {self.tablename} WHERE id_product=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Location(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def find_by_name(self, name):
        statement = f"SELECT id_product, name, direction, price, status FROM {self.tablename} WHERE name=?"
        self.cursor.execute(statement, (name,))
        result = self.cursor.fetchone()
        if result:
            return Client(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, direction, price, status) VALUES (?, ?, ?, ?)"
        self.cursor.execute(statement, (obj.name, obj.direction, obj.price, obj.status))
        try:
            self.connection.commit()
        except Exception as err:
            raise DbCommitException(err.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as err:
            raise DbUpdateException(err.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


connection = sqlite3.connect('patterns.sqlite')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'client': ClientMapper,
        'direction': DirectionMapper,
        'location': LocationMapper,
    }

    @staticmethod
    def get_mapper(obj):
        print(f"ой ой{obj.__class__}")
        if isinstance(obj, Client):
            print("дадада")
            return ClientMapper(connection)
        #if isinstance(obj, Category):
            #return CategoryMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
