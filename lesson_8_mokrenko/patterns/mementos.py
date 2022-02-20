'''
Модуль содержит реализацию поведенческого паттерна "Хранитель"
'''
from jsonpickle import dumps, loads

class BaseSerializer:


    def __init__(self, obj):
        self.obj = obj

    def save(self):
        print(f'Сериализуем объект {self.obj}')
        return dumps(self.obj)

    @staticmethod
    def load(data):
        print(f'Десериализуем объект из {data}')
        return loads(data)
