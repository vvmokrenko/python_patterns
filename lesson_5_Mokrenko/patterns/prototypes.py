from copy import deepcopy


class TaskPrototype:
    '''
        Метод для демонстрации порождающего паттерна "Прототип"
    '''
    #  Искусственный первичный ключ (можно использовать хэш)
    pk_id = 0

    def clone(self, new_pk=True):
        cl = deepcopy(self)
        if new_pk:
            TaskPrototype.pk_id += 1
            cl.id = TaskPrototype.pk_id
        return cl