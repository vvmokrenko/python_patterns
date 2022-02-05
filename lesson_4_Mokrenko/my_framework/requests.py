from quopri import decodestring

'''
Классы для обработки GET и POST-запросов нашим фреймворком
'''


def decode_value(data):
    '''
    Утилита обработки данных
    '''
    new_data = {}
    if data:
        for k, v in data.items():
            # готовим данные для приема процедурой decodestring
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            # print(val)
            # переводим полученные данные в кодировку UTF-8
            val_decode_str = decodestring(val).decode('UTF-8')
            # print(val_decode_str)
            new_data[k] = val_decode_str
        # print(f'Сработала процедура decode_value. На входе {data}, на выходе {new_data}')
    return new_data


def parse_input_data(data: str):
    '''
    Утилита обработки строки для получения словаря параметров
    Каждая пара ключ=значение разделяется символом &.
    Ключ от значения разделяется символом =
    '''
    result = {}
    if data:
        # делим параметры через &
        params = data.split('&')
        for item in params:
            # делим ключ и значение через =
            k, v = item.split('=')
            result[k] = v
        # print(f'Обработали строку {data}, возвращаем словарь {result}')

    return result

class GetRequest:
    '''
    Класс для обработки запросов типа GET
    '''

    def get_request_params(self, environ):
        '''
        Утилита парсинга значения перемнной окружения 'QUERY_STRING'
        '''
        # получаем параметры запроса
        query_string = environ['QUERY_STRING']
        # превращаем параметры в словарь
        request_params = parse_input_data(query_string)
        return request_params


class PostRequest:
    '''
    Класс для обработки запросов типа POST
    '''

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        '''
        Метод извлекает из внутренностей environ POST-данные в виде байтов
        '''
        # получаем длину тела
        content_length_data = env.get('CONTENT_LENGTH')
        # приводим к int
        content_length = int(content_length_data) if content_length_data else 0
        # print(content_length)
        # считываем данные, если они есть
        # env['wsgi.input'] -> <class '_io.BufferedReader'>
        # запускаем режим чтения

        data = env['wsgi.input'].read(content_length) \
            if content_length > 0 else b''
        return data

    @staticmethod
    def parse_wsgi_input_data(data: bytes) -> dict:
        result = {}
        if data:
            # print(f'строка до encoding utf8 - {data}')
            # декодируем данные
            data_str = data.decode(encoding='utf-8')
            # print(f'строка после encoding utf8 - {data_str}')
            # собираем их в словарь
            result = parse_input_data(data_str)
        return result


    def get_request_params(self, environ):
        # получаем данные в виде байтов
        data = self.get_wsgi_input_data(environ)
        # превращаем данные в байтах в словарь
        data = self.parse_wsgi_input_data(data)
        return data
