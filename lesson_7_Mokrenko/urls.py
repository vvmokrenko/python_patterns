from datetime import date
from views import Index, About, Contact, Heap, Registration, CreateTaskHeaped, CreateTaskScheduled


# front controller
def secret_front(request):
    request['date'] = date.today()

def other_front(request):
    request['key'] = 'some fc has done'


fronts = [secret_front, other_front]


""" 
Закомментированные маршруты реализованы через декораторы AppRoute (по аналогии как это сделано во Flask
"""
urls_routes = {
    # '/': Root(),
    '/index/': Index(),
    # '/heap/': Heap(),
    # '/about/': About(),
    # '/contact/': Contact(),
    '/registration/': Registration(),
    '/create-task-heaped/': CreateTaskHeaped(),
    '/create-task-scheduled/': CreateTaskScheduled(),
}
