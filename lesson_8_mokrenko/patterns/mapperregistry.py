'''
Модуль содержит классы, реализующие системный паттерн - Data Mapper
'''
from sqlite3 import connect
from patterns.tasks import Task, TaskScheduled, TaskHeaped

# работаем с единственной бд
connection = connect('db_mokrenko.sqlite')


# Примечание:
# Для того, чтобы указать объекты каких классов будут регистрироваться в UoW
# в модуле tasks.py класс task наследуем от DomainObject

class TaskMapper:
    '''
    Базовый класс для работы с моделью "Задача"
    '''

    table_map = {
        'task':           Task,
        'task_scheduled': TaskScheduled,
        'task_heaped':    TaskHeaped
    }


    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'task'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            # print(f'item from {self.tablename} -> {item}')
            # id, name, comment, priority, isexecuted, category, plandate, plantime, facttime = item
            task = self.table_map[self.tablename](*item[1:])
            # task.id = id
            task.id = item[0]
            result.append(task)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name, comment, category, priority FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            t = self.table_map[self.tablename](result[1], result[2], result[3], result[4])
            t.id = id
            return t
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        print('INSERT -->', type(obj), self.tablename, obj.name)
        statement = f"INSERT INTO {self.tablename} (name, comment, category, priority) VALUES (?, ?, ?, ?)"
        self.cursor.execute(statement, (obj.name, obj.comment, obj.category, obj.priority))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        print(f'DELETE {obj.name}')
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)



class TaskScheduledMapper(TaskMapper):

    def __init__(self, connection):
        super().__init__(connection)
        self.tablename = 'task_scheduled'


class TaskHeapedMapper(TaskMapper):

    def __init__(self, connection):
        # print('TaskHeapedMapper init')
        super().__init__(connection)
        self.tablename = 'task_heaped'



# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'task':           TaskMapper,
        'task_scheduled': TaskScheduledMapper,
        'task_heaped':    TaskHeapedMapper
    }

    @staticmethod
    def get_mapper(obj):
        # print('get_mapper', obj)

        if isinstance(obj, TaskScheduled):
            # print('get_mapper', '2')
            return MapperRegistry.mappers['task_scheduled'](connection)
        elif isinstance(obj, TaskHeaped):
            # print('get_mapper', '3')
            return MapperRegistry.mappers['task_heaped'](connection)
        elif isinstance(obj, Task):
            # print('get_mapper', '1')
            return MapperRegistry.mappers['task'](connection)


    @staticmethod
    def get_current_mapper(name):
        # print(f'{MapperRegistry.mappers}')
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
