'''
ДВИЖОК ДЛЯ НАПОЛНЕНИЯ САЙТА
'''

from patterns.tasks import TaskScheduled, TaskHeaped
from patterns.factories import TaskFactory


class Engine:
    def __init__(self):
        self.TasksScheduled =\
            [TaskScheduled('Сделать домашнее задание по курсу "Python"', 'Есть вопрос по ДЗ', 3, 2, True),
             TaskScheduled('Заказать корм коту с наименьшей ценой', 'В почте есть промокод. Найти.', 2, 1, False),
             TaskScheduled('Проверить личную почту', 'Жду письмо от ALiexpress', 1, 3, False),
             TaskScheduled('Сходить и получить посылку №121232312323', 'Почта работает и в ВСК', 2, 2, False)
            ]

        self.TasksHeaped = \
            [TaskHeaped('Сделать домашнее задание к уроку 2', 'Предварительно должно быть сделано ДЗ к уроку 1', 3, 1),
             TaskHeaped('Разобрать лоджию', 'Нужно дождаться тепла', 2, 3)
            ]

        self.courses = []
        self.categories = []

    @staticmethod
    def create_task(type, name, comment):
        return TaskFactory.create('heaped', name, comment)


    def find_task_heaped_by_id(self, id):
        for item in self.TasksHeaped:
            if item.id == int(id):
                return item
        raise Exception(f'Нет категории с id = {id}')
