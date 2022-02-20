'''
Классы для реализации примера поведенческого паттерна "Шаблонный метод"
'''

from my_framework.templator import render


class TemplateView:
    '''
    Базовый класс. Определяет методы получения контекста, шаблона (страницы),
    отрисовки страницы с передачей контекста, переопределяет вызов объекта.
    '''
    template_name = 'template.html'
    context_object_name = 'objects'

    # получаем данные контекста для передачи в шаблон страницы
    def get_context_data(self):
        return {}

    # получаем имя шаблона страницы
    def get_template(self):
        return self.template_name

    # рендерим шаблон (страницу) передавая туда данные их контекста
    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    # при вызове объекта вызываем рендеринг шаблона (страницы)
    def __call__(self, request):
        return self.render_template_with_context()

    # имя контекста для отрисовки на странице
    def get_context_object_name(self):
        return self.context_object_name

class ListView(TemplateView):
    '''
    Класс для определения списка.
    '''
    queryset = []
    template_name = 'list.html'


    # данные для списка
    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def set_queryset(self, data):
        self.queryset = data

    # переопределяем метод получения данных для формирования словаря-контекста
    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    '''
    Класс для определения формы ввода.
    '''
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)
