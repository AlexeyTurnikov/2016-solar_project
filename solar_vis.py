# coding: utf-8
# license: GPLv3
import pygame

pygame.init()
"""Модуль визуализации.
Функции, создающие гaрафические объекты и перемещающие их на экране, принимают физические координаты
"""

header_font = pygame.font.SysFont('Arial', 16)
"""Шрифт в заголовке"""

window_width = 600
"""Ширина окна"""

window_height = 600
"""Высота окна"""

"""
Масштабирование экранных координат по отношению к физическим.
Тип: float
Мера: количество пикселей на один метр.
"""


def calculate_scale_factor(max_distance):
    """Вычисляет значение scale_factor по данной характерной длине"""
    scaling = 0.4 * min(window_height, window_width) / max_distance
    return scaling


def scale_coord(body, coord, scale_factor, x_or_y):
    """Возвращает экранную координаты по координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.

    Параметры:
    :param body: тело, для которого происходит скейл координаты.
    :param coord: изначальная координата тела в физической СО.
    :param scale_factor: фактор скейлинга.
    :param x_or_y: Подана координата по х или по у? ==1 если х, ==0 если y.
    :returns: position - позиция, на которой необходимо отобразить тело.
    """
    if x_or_y == 0:
        position_corrector = window_width
    else:
        position_corrector = window_height
    r = body.get_r()
    position = - int(coord * scale_factor) + position_corrector // 2
    if position >= position_corrector - r:
        position = position_corrector + r
    if position <= r:
        position = -2 * r
    return position


def update_object_position(space, body, max_distance):
    """Создаёт отображаемый объект звезды.

    Параметры:

    **space** — холст для рисования.
    **star** — объект звезды.
    """
    scale_factor = calculate_scale_factor(max_distance)
    x = scale_coord(body, body.get_x(), scale_factor, 1)
    y = scale_coord(body, body.get_y(), scale_factor, 0)
    r = body.get_r()
    color = body.get_color()
    pygame.draw.circle(space, color, (x, y), r)


def update_system_name(space, system_name):
    """Создаёт на холсте текст с названием системы небесных тел.
    Если текст уже был, обновляет его содержание.
    Параметры:
    **space** — холст для рисования.
    **system_name** — название системы тел.
    """
    words = header_font.render(system_name, True, (0, 0, 0))
    place = words.get_rect(center=(30, 80))
    space.blit(words, place)


if __name__ == "__main__":
    print("This module is not for direct call!")
