class My:
    queryset = 'cla'
    def __init__(self):
        self.queryset = 'self'

    # данные для списка
    def get_queryset(self):
        return self.queryset
    @classmethod
    def get_clsqueryset(cls):
        return cls.queryset


a = My()
print(a.queryset)
print(a.get_queryset())
print(a.get_clsqueryset())
