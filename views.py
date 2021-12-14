from framework.templator import render
from patterns.behavioral_patterns import Subject

from patterns.make_patterns import Logger, Engine, Direction, WorkplaceAdmin
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, BaseSerializer
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import ListView

site = Engine()
logger = Logger('main')

# Элемент для варианта с Декораторами
routes = {}


# @AppRoute(routes=routes, url='/index/')
class Index:
    @Debug(name='Index', logger=logger)
    def __call__(self, request):
        # Добаавляем request 'list_locations'
        def selection(id_, request_):
            '''
            Функция делает выборку по направлению
            и заносит полученный список в request
            для вывода на странице
            '''
            list_ = site.find_direction_by_param(site.directions, int(id_)).locations
            request_['catalog'] = list_

        # Список функций обработчиков
        functions_dict = {
            'id_direction': selection,
        }

        request['catalog'] = site.catalog.goods_list

        directions_list = site.directions
        # Словарь, содержащий данные (словари) из GET-запроса
        get_dict = request.get('data_get')
        # Запуск обработчиков словарей GET-запросов
        if get_dict:
            for key in get_dict.keys():
                functions_dict[key](get_dict.get(key), request)
        return '200 OK', render('index.html', context=request,
                                directions=directions_list)


# @AppRoute(routes=routes, url='/basket-CBV/')
# class BasketCBV(ListView):
#     template_name = 'basket.html'
#     queryset = site.cart.list_for_html
#     context_object_name = 'cart'


@AppRoute(routes=routes, url='/basket/')
class Basket:
    @Debug(name='Basket', logger=logger)
    def __call__(self, request):
        request['cart'] = site.cart.goods_list

        directions_list = site.directions

        return '200 OK', render('basket.html', context=request, directions=directions_list)


@AppRoute(routes=routes, url='/history/')
class History:
    @Debug(name='History', logger=logger)
    def __call__(self, request):
        return '200 OK', render('history.html', context=request)


@AppRoute(routes=routes, url='/admin/')
class Admin:
    @Debug(name='Admin', logger=logger)
    def __call__(self, request):

        # Класс функций обработки событий
        workplace = WorkplaceAdmin(site, request)

        # Словарь обработки
        functions_dict = {
            'new_direction': workplace.create_new_direction,
            'delete_direction': workplace.delete_direction,
            'new_location': workplace.new_location,
        }

        # Словарь - данные POST-запроса
        post_dict = request.get('data_post')
        # Обработчик данных POST-запроса по словарю
        if post_dict:
            for key in post_dict.keys():
                if key in functions_dict:
                    functions_dict[key](post_dict.get(key))
            workplace.notify()

        request['list_directions'] = site.get_list_directions_names()
        return '200 OK', render('admin.html', context=request)


@AppRoute(routes=routes, url='/load_all/')
class AllProducts:
    @Debug(name='AllProducts', logger=logger)
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.catalog.goods_list).save()


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# Страница 'Список клиентов'
@AppRoute(routes=routes, url='/client-list/')
class ClientListView(ListView):
    queryset = site.users
    template_name = 'client-list.html'

