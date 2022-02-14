from my_framework.templator import render
from patterns.singletons import Logger  # порождающий паттерн singleton
from models.engine import Engine
from my_framework.requests import parse_input_data
from patterns.decorators import AppRoute, Debug
from patterns.mementos import BaseSerializer
from patterns.observers import Subject, EmailNotifier, SmsNotifier
from patterns.templatemethods import ListView, CreateView
from patterns.architectural_system_pattern_unit_of_work import UnitOfWork
from patterns.mapperregistry import MapperRegistry
from patterns.mapperregistry import TaskMapper, TaskHeapedMapper, TaskScheduledMapper

# Используем логирование информация в лог с именем main
logger = Logger('main')
# Инициализируем движок, который будет связывать наши шаблоны с данными
site = Engine()

routes = {}

email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

# Устанавливаем поток для сохранения измененных данных в БД и их получения
UnitOfWork.new_current()
# Связываем поток с нашим паттерном Data Mapper, который будет обслуживать обновление таблиц в БД
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@AppRoute(routes=routes, url='/')
class Root:
    @Debug(name='Root')
    def __call__(self, request):
        logger.log(self.__class__)

        # используем DB в качестве источника
        # tasks = site.TasksScheduled
        mapper = MapperRegistry.get_current_mapper('task_scheduled')
        tasks = mapper.all()

        return '200 OK', render('index.html', date=request.get('date', None), objects=tasks)


class Index:
    @Debug(name='Index')
    def __call__(self, request):
        logger.log(self.__class__)

        # используем DB в качестве источника
        # tasks = site.TasksScheduled
        mapper = MapperRegistry.get_current_mapper('task_scheduled')
        tasks = mapper.all()

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

        # используем DB в качестве источника
        # tasks = tasks = site.TasksHeaped
        mapper = MapperRegistry.get_current_mapper('task_heaped')
        tasks = mapper.all()

        return '200 OK', render('heap.html', objects=tasks)


@AppRoute(routes=routes, url='/all-task-list/')
class TaskListView(ListView):
    template_name = 'tasklist.html'

    def get_queryset(self):
        mapper1 = MapperRegistry.get_current_mapper('task_scheduled')
        tasks1 = mapper1.all()
        mapper2 = MapperRegistry.get_current_mapper('task_heaped')
        tasks2 = mapper2.all()
        return tasks1 + tasks2


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

            mapper = MapperRegistry.get_current_mapper('task_heaped')
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
                # маркируем объект как новый для последующего insert в базу
                # print(f'Anew_task -> {new_task}')
                new_task.mark_new()
                UnitOfWork.get_current().commit()

            # обновляем данные на странице
            tasks = mapper.all()

            # print(f'LEN={len(site.TasksHeaped)}')
            # return '200 OK', render('heap.html', objects=site.TasksHeaped)
            return '200 OK', render('heap.html', objects=tasks)


@AppRoute(routes=routes, url='/create-task-heaped-cbv/')
class TaskHeapedCreateView(CreateView):
    template_name = 'heap.html'

    def create_obj(self, data: dict):
        taskname = data['taskname']
        notes = data['notes']
        new_task = None

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
            # маркируем объект как новый для последующего insert в базу
            new_task.mark_new()
            UnitOfWork.get_current().commit()

    def get_context_data(self):
        context = super().get_context_data()
        context_object_name = self.get_context_object_name()
        mapper = MapperRegistry.get_current_mapper('task_heaped')
        tasks = mapper.all()
        #  context[context_object_name] = site.TasksHeaped
        context[context_object_name] = tasks
        return context


# контроллер - запланировать задачу на завтра
class CreateTaskScheduled:
    @Debug(name='CreateTaskScheduled')
    def __call__(self, request):
        # Создаем задачу в куче
        if request['method'] == 'POST':
            data = request['data']
            val = data['task_id']
            mapper = MapperRegistry.get_current_mapper('task_heaped')
            # Ищем чрез DM
            # task = site.find_task_heaped_by_id(val)
            task = mapper.find_by_id(val)
            # маркируем объект как удаленный
            task.mark_removed()
            UnitOfWork.get_current().commit()
            tasks = mapper.all()
            # Добавляем в расписание
            # new_task = task.clone(False)
            new_task = site.create_task('scheduled', task.name, task.comment)
            new_task.category = task.category
            new_task.priority = task.priority
            # print(f' В задачу {new_task.name}, {new_task.id}')

            # не нужно site.TasksScheduled.append(new_task)
            # определяем по умолчанию подписчиков для объектов-издателей нашего клаcса
            new_task.observers.append(email_notifier)
            new_task.observers.append(sms_notifier)
            new_task.notify()

            # маркируем объект как новый для последующего insert в базу
            new_task.mark_new()
            UnitOfWork.get_current().commit()

            # print(f'LEN TS={len(site.TasksScheduled)}')
            # print(f'LEN TH={len(site.TasksHeaped)}')
            # return '200 OK', render('heap.html', objects=site.TasksHeaped)
            return '200 OK', render('heap.html', objects=tasks)


@AppRoute(routes=routes, url='/save_to_json/')
class SaveToJson:
    @Debug(name='SaveToJson')
    def __call__(self, request):
        mapper = MapperRegistry.get_current_mapper('task_heaped')
        tasks = mapper.all()
        # site.serialized = BaseSerializer(site.TasksHeaped).save()
        site.serialized = BaseSerializer(tasks).save()
        return '200 OK', site.serialized


@AppRoute(routes=routes, url='/upload_from_json/')
class UploadFromJson:
    @Debug(name='UploadFromJson')
    def __call__(self, request):
        src = BaseSerializer.load(site.serialized)
        mapper = MapperRegistry.get_current_mapper('task_heaped')
        tasks = mapper.all()
        # site.TasksHeaped = site.TasksHeaped + src
        # return '200 OK', render('heap.html', objects=site.TasksHeaped)
        tasks = tasks + src
        return '200 OK', render('heap.html', objects=tasks)
