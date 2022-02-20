from my_framework.main import Framework
from urls import routes, fronts

def application(environ, start_response):

    app = Framework(routes, fronts)

    return app(environ, start_response)
