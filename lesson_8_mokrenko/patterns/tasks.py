import datetime
from patterns.prototypes import TaskPrototype
from patterns.observers import Subject, EmailNotifier, SmsNotifier
from patterns.architectural_system_pattern_unit_of_work import DomainObject




class Category:
    '''
    Класс Категория задач
    '''

    categories = {1: 'Работа',
                  2: 'Дом',
                  3: 'Учеба',
                  4: 'Бэклог'}

    @staticmethod
    def get_default():
        return 4

    @staticmethod
    def get_name(id):
        return Category.categories[id]


class Priority:
    '''
    Класс Приоритет задачи
    '''

    priorities = {1: 'Critical',
                  2: 'Major',
                  3: 'Normal'}

    @staticmethod
    def get_default():
        return 3

    @staticmethod
    def get_name(id):
        return Priority.priorities[id]



class Task(TaskPrototype, Subject, DomainObject):
    '''
    Абстрактный класс Задача
    '''


    def __init__(self, name, comment='',category=Category.get_default(), priority=Priority.get_default(), isexecuted=False):
        TaskPrototype.pk_id += 1
        self.id = TaskPrototype.pk_id
        self.name = name  # имя задачи
        self.comment = comment # комментарий к задаче
        self.priority = priority
        if priority:
            self.priority_name = Priority.get_name(self.priority)
        self.isexecuted = isexecuted
        self.category = category
        if category:
            self.category_name = Category.get_name(self.category)
        super().__init__()




class TaskScheduled(Task):
    '''
    Класс Запланированная задача
    '''
    def __init__(self, name, comment='', category=Category.get_default(), priority=Priority.get_default(),
                 isexecuted=False, plandate=datetime.date, plantime=int(), facttime=int()):
        super().__init__(name, comment, category, priority, isexecuted)
        self.plandate = plandate
        self.plantime = plantime
        self.facttime = facttime



class TaskHeaped(Task):

    '''
    Класс Задача из кучи
    '''
    def __init__(self, name, comment='', category=Category.get_default(), priority=Priority.get_default(), target_date=None):
        super().__init__(name, comment, category, priority)
        self.target_date = target_date



if __name__ == '__main__':
    t = TaskScheduled('Сделать домашнее задание по курсу "Python"', 'Есть вопрос по ДЗ', 3, 2, True)
    print(t)
    h = TaskHeaped('Сделать домашнее задание к уроку 2', 'Предварительно должно быть сделано ДЗ к уроку 1', 3, 1)
    print(h)