
from .requests import GetRequest, PostRequest, decode_value

class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:

    """Класс Framework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        path = environ['PATH_INFO']

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'


        # Обрабатываем входные сообщения, получаемые от сервера
        request = {}
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        # Запоминаем метод в нашем словаре
        request['method'] = method

        # print(environ)

        # Обрабатываем параметры только, если не пришли "левые" адреса, чтобы не засорять вывод информацией
        if not path.endswith('.png/'):
            if method == 'POST':
                data = PostRequest().get_request_params(environ)
                request['data'] = decode_value(data)
                print(f"Нам пришёл POST-запрос от страницы {path} cо следующими данными\n: {request['data']}")

            if method == 'GET':
                request_params = GetRequest().get_request_params(environ)
                request['request_params'] = decode_value(request_params)
                if request['request_params']:
                    print(f"Нам пришли GET-параметры от страницы {path}: {request['request_params']}")

        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts_lst:
            front(request)
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
