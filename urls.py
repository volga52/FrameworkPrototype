from datetime import date

from views import Index, Basket, History, IndexNew, Admin
from variables import DIRECTION


# front controllers
def secret_front(request):
    request['data'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/index.html/': Index(),
    '/index-new.html/': IndexNew(),
    '/basket.html/': Basket(),
    '/history.html/': History(),
    '/admin.html/': Admin(),
}
