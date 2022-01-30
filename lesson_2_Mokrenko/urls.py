from datetime import date
from views import Index, About, Contact, Heap, Registration


# front controller
def secret_front(request):
    request['date'] = date.today()

def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/index/': Index(),
    '/heap/': Heap(),
    '/about/': About(),
    '/contact/': Contact(),
    '/registration/': Registration(),
}
