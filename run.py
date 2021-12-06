from framework.main import Framework
from urls import routes, fronts
from wsgiref.simple_server import make_server
from patterns.make_patterns import Logger

logger = Logger('run')
application = Framework(routes, fronts)

with make_server('', 8081, application) as httpd:
    logger.log("Запуск, задействован порт 8081...")
    # print("Запуск, задействован порт 8081...")
    httpd.serve_forever()
