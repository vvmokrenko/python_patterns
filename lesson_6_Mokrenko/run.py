from wsgiref.simple_server import make_server

from my_framework.main import Framework
from urls import urls_routes, fronts
from views import routes

# Объединяем маршруты из модуля URL (как в Django) и модуля VIEW (как во Flask)
print(f'Маршруты а-ля Django: {urls_routes}')
print(f'Маршруты а-ля Flask: {routes}')
all_routes = {**urls_routes, **routes}
print(f'Маршруты, обрабатываемые нашим фреймворком: {all_routes}')

application = Framework(all_routes, fronts)

with make_server('', 8080, application) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()
