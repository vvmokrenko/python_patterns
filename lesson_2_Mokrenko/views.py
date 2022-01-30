from my_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


class About:
    def __call__(self, request):
        return '200 OK', render('about.html')


class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html')


class Heap:
    def __call__(self, request):
        return '200 OK', render('heap.html')


class Registration:
    def __call__(self, request):
        return '200 OK', render('registration.html')