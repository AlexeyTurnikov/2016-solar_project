# coding: utf-8
# license: GPLv3

import pygame
from tkinter.filedialog import *
import solar_vis as vis
import solar_model as model
import solar_input

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

physical_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

displayed_time = None
"""Отображаемое на экране время.
Тип: переменная tkinter"""

time_step = None
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""
HEIGHT = 800
WIDTH = 600
FPS = 30
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
GREY = (128, 128, 128)
RED = (200, 50, 100)
WHITE = (255, 255, 255)


def writing(text: str, xcenter, ycenter, font_size=16):
    font = pygame.font.SysFont('Arial', font_size)
    words = font.render(text, True, (0, 0, 0))
    place = words.get_rect(center=(xcenter, ycenter))
    SCREEN.blit(words, place)


class Button:

    def __init__(self, x, y, length, width, text: str, ):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.text = text
        self.color = GREY
        self.pressed = FALSE
        self.timer = 0

    def draw(self):
        if self.pressed is TRUE:
            self.color = RED
        else:
            self.color = GREY
        pygame.draw.rect(SCREEN, self.color, (self.x, self.y, self.length, self.width))
        if self.timer > 0:
            self.timer += 1
        if self.timer % 30 == 0:
            self.pressed = False
        writing(self.text, self.x + self.length / 2, self.y + self.width / 2)

    def is_button_pressed(self, event):
        if self.x < event.pos[0] < self.x + self.length and self.y < event.pos[1] < self.y + self.width:
            self.pressed = TRUE
            self.timer = 1
            print("pressed")


class Timer(Button):
    def __init__(self, x, y, length, width, text: str):
        super().__init__(x, y, length, width, text)
        self.time = "1"

    def draw(self):
        super().draw()
        writing(self.time, self.x + self.length / 2, self.y + 2 * self.width / 3)

    def update(self, event):
        if event.key == pygame.K_BACKSPACE and len(self.time) >= 1:
            self.time = self.time[:-1]
        elif len(self.time) <= 10:
            self.time += event.unicode
            self.time = "".join(c for c in self.time if c.isdecimal())  # проверяет введена ли цифра

    def set_physical_time(self):
        time_step = int(self.time)
        return time_step


def save_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    solar_input.write_space_objects_data_to_file(out_filename, space_objects)


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    pygame.init()
    print('Modelling started!')
    physical_time = 0
    start = 1
    distances =[]
    finished = False

    start_button = Button(0, 600, 100, 200, "start")
    timer = Timer(100, 600, 200, 200, "time:")
    load_from_file_button = Button(300, 600, 150, 200, "load_from_file")
    save_file_button = Button(450, 600, 150, 200, "save_file")
    buttons = [start_button, load_from_file_button, save_file_button]

    objects = solar_input.read_space_objects_data_from_file("solar_system.txt")
    for object in objects:
        distances.append(max(abs(object.get_x()), abs(object.get_y())))
    max_distance = max(distances)


    while not finished:
        clock.tick(FPS)
        SCREEN.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    button.is_button_pressed(event)
                    if start_button.pressed is True:
                        start = 1
            if event.type == pygame.KEYDOWN:
                timer.update(event)
        for button in buttons:
            button.draw()

        if start == 1:

            for object in objects:
                model.recalculate_space_objects_positions(objects, timer.set_physical_time())
                vis.update_object_position(SCREEN, object, max_distance)
                vis.image(SCREEN, object, max_distance)

        timer.draw()
        pygame.display.update()

    print('Modelling finished!')


if __name__ == "__main__":
    main()
