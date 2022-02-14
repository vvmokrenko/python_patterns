'''
РЕАЛИЗАЦИЯ ПАТТЕРНА SINGLETON
SingletonByName(type) - будет метаклассом, который инициализируется ТОЛЬКО 1 РАЗ при любом количестве
вызовов класса. Поэтому словарь cls.__instance инициализируется именно в конструкторе.
Имя класса-потомка содержится в атрибуте classname конструктора. То есть сколько бы мы не определили
классов, основанных на SingletonByName, все эти классы будут шарить один cls.__instance
'''
from patterns.strategies import ConsoleWriter, FileWriter

# установка логирования. Логирование возможно в файл (FileWriter) и консоль (ConsoleWriter).
# по умолчанию пишем в файл
GLOBAL_LOGGER_ON = True

class SingletonByName(type):

    #  вызывается только один раз. name - это имя класса
    def __init__(cls, classname, bases, attrs, **kwargs):
        # print(f'SingletonByName __init__ {classname} {bases} {attrs}')
        super().__init__(classname, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        # print(f'SingletonByName __call__ {args}')
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=FileWriter()):
        # print('Logger __init__')
        self.name = name
        self.writer = writer

    def log(self, text):
        if GLOBAL_LOGGER_ON:
            print(f'Запись в лог {self.name}--->', text)
            self.writer.write(text)


# Отладка
if __name__ == '__main__':
    logger = Logger('main')
    logger1 = Logger('main1')

    logger.log(f'Тестовая запись')
    logger1.log(f'Тестовая запись')
