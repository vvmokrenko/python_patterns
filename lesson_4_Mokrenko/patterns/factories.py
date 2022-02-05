from patterns.tasks import Task, TaskScheduled, TaskHeaped

class TaskFactory:
    '''
    Класс для демонстрации порождающего паттерна "Фабричный метод"
    '''
    types = {
        'simple':    Task,
        'scheduled': TaskScheduled,
        'heaped':    TaskHeaped
    }

    @classmethod
    def create(cls, tasktype, taskname, taskcomment=''):
        return cls.types[tasktype](taskname, taskcomment)


