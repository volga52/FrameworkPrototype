# import os
import jsonpickle

from framework.templator import render


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


# поведенческий паттерн - Шаблонный метод
class TemplateView:
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        # print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data_post']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request.get('data_post', None) and request['data_post']['new_user_name']:
            # метод пост
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)
