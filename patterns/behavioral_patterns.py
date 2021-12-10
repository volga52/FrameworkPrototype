class Subject:

    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class Observer:

    def update(self, subject):
        pass


class SmsNotifier(Observer):

    def update(self, subject):
        print('SMS->', f'в диеркторию {subject.public_name} добавлен '
                       f'объект ', subject.locations[-1].name)


class EmailNotifier(Observer):

    def update(self, subject):
        print('EMAIL->', f'в диеркторию {subject.public_name} добавлен '
                         f'объект ', subject.locations[-1].name)
