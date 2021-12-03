from datetime import date

from views import Index, Basket, History, Admin


# front controllers
def secret_front(request):
    request['data'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/index/': Index(),
    '/basket/': Basket(),
    '/history/': History(),
    '/admin/': Admin(),
}
