'''
Модуль содержит реализацию поведенческого паттерна "Стратегия"
'''
class ConsoleWriter:

    def write(self, text):
        print(f'ConsoleWriter --> {text}')


class FileWriter:

    def __init__(self):
        self.file_name = 'log'

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            print(f'FileWriter в файл {self.file_name} --> {text}')
            f.write(f'{text}\n')
