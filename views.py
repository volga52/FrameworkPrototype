from framework.templator import render

from base_product import Catalog
from patterns.make_patterns import Logger


site = Catalog()
logger = Logger('main')
# CATALOG = 'catalog'


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', context=request)


class Basket:
    def __call__(self, request):
        return '200 OK', render('basket.html', context=request)


class History:
    def __call__(self, request):
        return '200 OK', render('history.html', context=request)


class Admin:
    def __call__(self, request):
        return '200 OK', render('admin.html', context=request)


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'



class IndexNew:
    def __call__(self, request):
        request['catalog'] = site.goods_list
        return '200 OK', render('index-new.html', context=request)
