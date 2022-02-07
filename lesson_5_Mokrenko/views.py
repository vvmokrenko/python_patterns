from my_framework.templator import render
from patterns.singletons import Logger  # порождающий паттерн singleton
from models.engine import Engine
from my_framework.requests import parse_input_data
from patterns.decorators import AppRoute, Debug

# Используем логирование информация в лог с именем main
logger = Logger('main')
# Инициализируем движок, который будет связывать наши шаблоны с данными
site = Engine()

routes = {}

@AppRoute(routes=routes, url='/')
class Root:
    @Debug(name='Root')
    def __call__(self, request):
        logger.log(self.__class__)
        tasks = site.TasksScheduled
        return '200 OK', render('index.html', date=request.get('date', None), objects=tasks)

class Index:
    @Debug(name='Index')
    def __call__(self, request):
        logger.log(self.__class__)
        tasks = site.TasksScheduled
        return '200 OK', render('index.html', date=request.get('date', None), objects=tasks)

@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        logger.log(self.__class__)
        return '200 OK', render('about.html')

@AppRoute(routes=routes, url='/contact/')
class Contact:
    @Debug(name='Contact')
    def __call__(self, request):
        logger.log(self.__class__)
        return '200 OK', render('contact.html')

@AppRoute(routes=routes, url='/heap/')
class Heap:
    @Debug(name='Heap')
    def __call__(self, request):
        logger.log(self.__class__)
        tasks = site.TasksHeaped
        return '200 OK', render('heap.html', objects=tasks)


class Registration:
    @Debug(name='Registration')
    def __call__(self, request):
        logger.log(self.__class__)
        return '200 OK', render('registration.html')



# контроллер - создать задачу в куче
class CreateTaskHeaped:
    @Debug(name='CreateTaskHeaped')
    def __call__(self, request):

        # Создаем задачу в куче
        if request['method'] == 'POST':
            data = request['data']

            taskname = data['taskname']
            notes = data['notes']

            #  Если имя задачи не пусто, то создаем ее, если пусто - создаем клон последней задачи
            if taskname:
                new_task = site.create_task('heaped', taskname, notes)
            else:
                if len(site.TasksHeaped) > 0:
                    last_task = site.TasksHeaped[-1]
                    new_task = last_task.clone()
                    new_name = f'copy_{last_task.name}'
                    new_task.name = new_name
                    new_task.comment = notes or last_task.comment

            if new_task:
                site.TasksHeaped.append(new_task)

            return '200 OK', render('heap.html', objects=site.TasksHeaped)


# контроллер - запланировать задачу на завтра
class CreateTaskScheduled:
    @Debug(name='CreateTaskScheduled')
    def __call__(self, request):

        # Создаем задачу в куче
        if request['method'] == 'POST':
            data = request['data']
            val = data['task_id']
            task = site.find_task_heaped_by_id(val)
            # Добавляем в расписание
            new_task = task.clone(False)

            site.TasksScheduled.append(new_task)
            site.TasksHeaped.remove(task)

            return '200 OK', render('heap.html', objects=site.TasksHeaped)
