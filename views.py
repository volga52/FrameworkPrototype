from framework.templator import render

from patterns.make_patterns import Logger, Engine


site = Engine()
logger = Logger('main')


class Index:
    def __call__(self, request):

        # Добаавляем request 'list_locations'
        def selection(id_, request_):
            '''
            Функция делает выборку по направлению
            и заносит полученный список в request
            '''
            list_ = [elem for elem in site.catalog.list_for_html if elem['direction'] == int(id_)]
            request_['catalog'] = list_

        # Список функций обработчиков
        functions_dict = {
            'id_direction': selection,
        }

        request['catalog'] = site.catalog.list_for_html

        # Преобразуем объект класса в список словарей
        directions_list = [vars(i) for i in site.directions]

        get_dict = request.get('data_get')
        if get_dict:
            for key in get_dict.keys():
                functions_dict[key](get_dict[key], request)

        print(request)

        return '200 OK', render('index.html', context=request,
                                directions=directions_list)


class Basket:
    def __call__(self, request):
        return '200 OK', render('basket.html', context=request)


class History:
    def __call__(self, request):
        return '200 OK', render('history.html', context=request)


class Admin:
    def __call__(self, request):
        request['list_directions'] = site.get_list_direction()
        return '200 OK', render('admin.html', context=request)


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - создать категорию
# class CreateDirection:
#     def __call__(self, request):
#
#         if request['method'] == 'POST':
#             # метод пост
#             print(request)
#             data = request['data']
#
#             name = data['name']
#             name = site.decode_value(name)
#
#             category_id = data.get('category_id')
#
#             category = None
#             if category_id:
#                 category = site.find_direction_by_id(int(category_id))
#
#             new_category = site.create_category(name, category)
#
#             site.categories.append(new_category)
#
#             return '200 OK', render('index.html', objects_list=site.categories)
#         else:
#             categories = site.categories
#             return '200 OK', render('create_category.html', categories=categories)

