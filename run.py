from framework.main import Framework
from urls import routes, fronts
from wsgiref.simple_server import make_server

application = Framework(routes, fronts)

with make_server('', 8081, application) as httpd:
    print("Запуск, задействован порт 8081...")
    httpd.serve_forever()
