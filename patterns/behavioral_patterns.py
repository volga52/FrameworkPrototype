import os

import jsonpickle


class Subject:

    def __init__(self):
        self.observers = []

    def notify(self):
        # _self = self
        for item in self.observers:
            # print(vars(self))
            item.update(self)


class Observer:

    def update(self, subject):
        pass


class SmsNotifier(Observer):

    # @staticmethod
    # def update(subject):
    def update(self, subject):
        loc = subject.site.catalog.goods_list[-1]
        directions = subject.site.directions
        print(
            'SMS->', f'в директорию '
            f'{subject.site.find_direction_by_param(directions, loc.direction).public_name}'
            f' добавлен объект ', {loc.name})


class EmailNotifier(Observer):

    # @staticmethod
    # def update(subject):
    def update(self, subject):
        loc = subject.site.catalog.goods_list[-1]
        directions = subject.site.directions
        print(
            'EMAIL->', f'в директорию '
            f'{subject.site.find_direction_by_param(directions, loc.direction).public_name}'
            f' добавлен объект ', {loc.name})


class BaseSerializer:
    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return jsonpickle.dumps(self.obj)

    @staticmethod
    def load(data):
        return jsonpickle.loads(data)


# # поведенческий паттерн - Стратегия
# class ConsoleWriter:
#     def __init__(self, name):
#         self.name = name
#
#     def write(self, text):
#         print(f'{self.name} log--> {text}')
#
#
# class FileWriter:
#
#     def __init__(self, name):
#         path = os.getcwd()
#         self.name = f"{path}\\logs\\{name}_log.log"
#
#     def write(self, text):
#         with open(self.file_name, 'a+', encoding='utf-8') as file:
#             file.write(f'{text}\n')

