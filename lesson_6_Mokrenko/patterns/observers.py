'''
Класс для реализации примера поведенческого паттерна "Наблюдатель"
'''
# Курс
class Observer:
    '''
        Класс определяет подписчиков(наблюдателей) ля получения данных об изменении состояния издателей.
    '''
    def update(self, subject):
        pass

class SmsNotifier(Observer):

    def update(self, subject):
        print(f'SMS -> на выполнение сегодня добавлена задача {subject.name}')


class EmailNotifier(Observer):

    def update(self, subject):
        print(f'EMAIL -> на выполнение сегодня добавлена задача {subject.name}')


class Subject:
    '''
    Класс определяет издателя для уведомления подписчиков(наблюдателей) об изменении своего состояния
    '''

    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)