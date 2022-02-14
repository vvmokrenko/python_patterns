from time import time


class Debug:
    '''
        Класс для демонстрации структурного паттерна Декоратор
        Добавляет функциональность замера времени
    '''

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        # это вспомогательная функция будет декорировать каждый отдельный метод класса, см. ниже
        def timeit(method):
            '''
            нужен для того, чтобы декоратор класса wrapper обернул в timeit
            каждый метод декорируемого класса
            '''

            print('Сработал декоратор: ', method)

            def timed(*args, **kw):
                ts = time()
                result = method(*args, **kw)
                te = time()
                delta = te - ts

                print(f'debug --> {self.name}.{method} выполнялся {delta:2.2f} ms')
                return result

            return timed

        return timeit(cls)


class AppRoute:
    '''
        Класс для демонстрации структурного паттерна Декоратор
        Добавляет новую функциональность, обеспечивающую связь url и контроллера (как во Flask)
    '''

    def __init__(self, routes, url):
        '''
        Сохраняем значение переданного параметра
        '''
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        '''
        Сам декоратор
        '''
        self.routes[self.url] = cls()
        print(f'Сработал декоратор для класса {cls()}. Слушаем адрес {self.url}. Список адресов: {self.routes}')

