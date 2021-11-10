# coding: utf-8
# license: GPLv3
import pygame

pygame.init()
"""Модуль визуализации.
Нигде, кроме этого модуля, не используются экранные координаты объектов.
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


def scale_x(body, x, scale_factor):
    """Возвращает экранную **x** координату по **x** координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода **x** координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.

    Параметры:

    **x** — x-координата модели.
    """
    r = body.get_r()
    position = - int(x * scale_factor) + window_width // 2
    if position >= window_width - r:
        position = window_width - r
    if position <= r:
        position = r
    return position


def scale_y(body, y, scale_factor):
    """Возвращает экранную **y** координату по **y** координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода **y** координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.
    Направление оси развёрнуто, чтобы у модели ось **y** смотрела вверх.

    Параметры:

    **y** — y-координата модели.
    """
    r = body.get_r()
    position = - int(y * scale_factor) + window_height // 2
    if position >= window_height - r:
        position = window_height - r
    if position <= r:
        position = r
    return position


def image(space, body, max_distance):
    """Создаёт отображаемый объект звезды.

    Параметры:

    **space** — холст для рисования.
    **star** — объект звезды.
    """
    scale_factor = calculate_scale_factor(max_distance)
    x = scale_x(body, body.get_x(), scale_factor)
    y = scale_y(body, body.get_y(), scale_factor)
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


def update_object_position(space, body, max_distance, dt):
    """Перемещает отображаемый объект на холсте.
    Параметры:
    **space** — холст для рисования.
    **body** — тело, которое нужно переместить.
    """
    scale_factor = calculate_scale_factor(max_distance)
    vx = body.get_vx()
    vy = body.get_vy()
    x = scale_x(body, body.get_x(), scale_factor) + vx*dt
    y = scale_y(body, body.get_y(), scale_factor) + vy*dt
    r = body.get_r()
    # ToDo возможно нужно убрать скорости, может повторять работу из solar_model

    body.set_x(x + body.get_x())
    body.set_y(y + body.get_y())
    image(space, body, max_distance)


if __name__ == "__main__":
    print("This module is not for direct call!")
