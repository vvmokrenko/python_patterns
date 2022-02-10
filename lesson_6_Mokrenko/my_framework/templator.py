from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    Используем вcтроенные методы jinja2 для формирования шаблона,
    указывая имя основного шаблона и папку, где находятся все шаблоны.
    Это позволяет шаблонизатору обрабатывать логику включения шаблонов.
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры
    :return:
    """

    # создаем объект окружения
    env = Environment()
    # указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(folder)
    # находим шаблон в окружении
    template = env.get_template(template_name)
    # рендерим шаблон с параметрами
    return template.render(**kwargs)
