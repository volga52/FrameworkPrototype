from datetime import date

from patterns.make_patterns import Logger
from views import Index, Basket, History, Admin


logger = Logger('front')


# front controllers
def secret_front(request):
    request['data'] = date.today()


def create_dict_new_location_front(request):
    '''
    Функция формирования данных для создания нового товара
    Преобразует несколько данных в один словарь для
    'Обработчика' страниц сайта
    '''
    data_post = request.get('data_post', None)
    if data_post \
            and data_post.get('make_name', None) \
            and data_post.get('make_direction', None):
        data_post['make_price'] = data_post.get('make_price', '0')

        data_list = (data_post['make_name'], data_post['make_direction'], int(data_post['make_price']))
        request['data_post']['new_location'] = data_list


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front, create_dict_new_location_front]

routes = {
    '/': Index(),
    '/index/': Index(),
    '/basket/': Basket(),
    '/history/': History(),
    '/admin/': Admin(),
}
