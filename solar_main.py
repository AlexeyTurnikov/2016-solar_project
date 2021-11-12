# coding: utf-8
# license: GPLv3

import pygame
import solar_vis as vis
import solar_model as model
import solar_input
from solar_objects import Star
import matplotlib.pyplot as plt

HEIGHT = 800  # Высота экрана

WIDTH = 600  # Ширина экрана

FPS = 30  # Количество кадров в секунду

# Цвета
GREY = (128, 128, 128)
RED = (200, 50, 100)
WHITE = (255, 255, 200)
BLACK = (0, 0, 0)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Button:
    """
    Класс, отвечающий за кнопки, которые создаются на экране.
    """

    def __init__(self, x, y, length, width, text: str, ):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.text = text
        self.color = GREY
        self.pressed = False  # Нажата ли кнопка?
        self.timer = 0  # время, прошедшее с нажатия на кнопку, кнопка горит 1 секунду после нажатия.

    def draw(self):
        """Функция, отвечающая за отрисовку кнопки на экране."""
        if self.pressed is True:  # Нажатая кнопка загорается красным
            self.color = RED
        else:
            self.color = GREY
        pygame.draw.rect(SCREEN, self.color, (self.x, self.y, self.length, self.width))
        pygame.draw.rect(SCREEN, BLACK, (self.x, self.y, self.length, self.width), 1)
        writing(self.text, self.x + self.length / 2, self.y + self.width / 2)
        if self.timer > 0:
            self.timer += 1
        if self.timer % 30 == 0:
            self.pressed = False

    def is_button_pressed(self, event):
        """
        Функция, проверяющая нажата ли кнопка.
        """
        if self.x < event.pos[0] < self.x + self.length and self.y < event.pos[1] < self.y + self.width:
            self.pressed = True
            self.timer = 1


class Timer(Button):
    """
    Подкласс Button, отличается наличием функции ввода времени.
    """

    def __init__(self, x, y, length, width, text: str):
        super().__init__(x, y, length, width, text)
        self.time = "1"

    def draw(self):
        super().draw()
        writing(self.time, self.x + self.length / 2, self.y + 2 * self.width / 3)

    def update(self, event):
        """
        Функция, отвечающая за ввод времени с клавиатуры, на вход принимаются только цифры.
        """
        if event.key == pygame.K_BACKSPACE and len(self.time) >= 1:
            self.time = self.time[:-1]
        elif len(self.time) <= 10:
            self.time += event.unicode
            self.time = "".join(symbol for symbol in self.time if symbol.isdecimal())  # проверяет введена ли цифра

    def set_time_step(self):
        """
        Функция, которая возвращает время введенное с клавиатуры.
        Возвращает шаг времени в физическом моделировании.
        """
        if len(self.time) >= 1:
            time_step = int(self.time)
        else:
            time_step = 1
        return time_step


def calculating_max_distance(objects):
    """
    Функция, отвечающая за рассчет максимального расстояния между телами.
    """
    distances = []
    for obj in objects:
        distances.append(max(abs(obj.get_x()), abs(obj.get_y())))
    return max(distances)


def writing(text: str, xcenter, ycenter, font_size=16):
    """Функция, отвечающая за вывод текста на экран
    :param text: текст, который будет выведен на экран
    :param xcenter: x координата центра
    :param ycenter: y координата центра
    :param font_size: размер шрифта, стандартный шрифт Arial
    """
    font = pygame.font.SysFont('Arial', font_size)
    words = font.render(text, True, (0, 0, 0))
    place = words.get_rect(center=(xcenter, ycenter))
    SCREEN.blit(words, place)


def statecheck(starting, pausing, loading, visualise, start, loading_file, visualising):
    """
    Проверяет, на какую из кнопок нажал пользователь.
    :param starting: кнопка, отвечающая за начало моделирования
    :param pausing: кнопка, отвечающая за приостановку моделирования
    :param loading: кнопка, отвечающая за загрузку нового файла
    :param visualise: кнопка, отвечающая за отображение графиков
    :param start: параметр, отвечающий за то началось ли моделирование
    :param loading_file: параметр, отвечающий за то началась ли загрузка нового файла
    :param visualising: параметр, отвечающий за то началась ли отрисовка графика

    """
    if starting.pressed is True:
        start = 1
        loading_file = 0
        visualising = 0
    if pausing.pressed is True:
        start = 0
        loading_file = 0
        visualising = 0
    if loading.pressed is True:
        start = 0
        loading_file = 1
        visualising = 0
    if visualise.pressed is True:
        start = 0
        loading_file = 0
        visualising = 1
    return start, loading_file, visualising


def save_planet_parameters(planet, physical_time):
    """
    Функция, которая сохраняет каждые 500000 лет данные о скорости и расстоянии до звезды у тела.
    :param planet: планета, для которой необходимо сохранить данные.
    :param physical_time: физическое время, прошедшее с начала моделирования.
    """
    i = 1
    if physical_time - i * 500000 > 0:
        planet.append_v_massive((planet.get_vx() ** 2 + planet.get_vy() ** 2) ** 0.5)
        planet.append_distance_massive((planet.get_x() ** 2 + planet.get_y() ** 2) ** 0.5)
        i += 1


def painting_graphics(planet):
    """
    Функция, отвечающая за работу с массивом скоростей, расстояний до звезды, отрисовку графиков.
    График рисуется по последним 100 точкам. Если точек меньше 100, то по всем точкам.
    :param planet: планета, для которой необходимо нарисовать графики
    """
    velocity = planet.get_v_massive()
    while len(velocity) > 100:
        velocity.pop(0)
    distance = planet.get_distance_massive()
    while len(distance) > 100:
        distance.pop(0)
    time = []
    if len(velocity) < 100:
        steps = len(velocity)
    else:
        steps = 100
    for timer in range(0, 300000 * steps, 300000):
        time.append(timer)
    plt.figure(figsize=(20, 10))
    plt.subplot(131)
    plt.plot(time, velocity)
    plt.title('$Velocity$')
    plt.xlabel("time, years", )
    plt.ylabel("velocity, km/years")
    plt.grid(True)
    plt.subplot(132)
    plt.plot(time, distance)
    plt.title(r'$Distance to planet$')
    plt.xlabel("time, years")
    plt.ylabel("distance, km")
    plt.grid(True)
    plt.subplot(133)
    plt.plot(distance, velocity)
    plt.title(r'$Distance/Velocity$,')
    plt.xlabel("distance, km")
    plt.ylabel("velocity, km/years")
    plt.grid(True)
    plt.show()


def visualising_process(objects, loaded_file, number_of_planet):
    """
    Функция, отвечающая за меню выбора планеты, для которой необходимо построить график.
    Также запускает отрисовку самого графика
    :param objects: массив со всеми телами в модели.
    :param loaded_file: файл, который сейчас моделируется.
    :param number_of_planet: номер планеты, для которой пользователь хочет увидеть графики.
    """
    visualising = 1
    start = 0
    names = ["Mercury", "Venus", "Earth", "Mars", "Jupyter", "Saturn", "Uranus", "Neptune"]
    writing("Введите номер выбранной планеты", 300, 100)
    if loaded_file == "solar_system.txt":
        for i in range(0, len(objects) - 1):
            writing(names[i] + " [ " + str(i) + " ] ", 300, 125 + i * 25)
    if loaded_file == "double_star.txt":
        writing("Ни один из обьектов", 300, 125)
        writing("не является планетой", 300, 150)
        if number_of_planet is not False:
            number_of_planet = False
            visualising = 0
            start = 1
    if loaded_file == "one_satellite.txt":
        writing("planet [0]", 300, 125)
    if (not str(number_of_planet).isdecimal() or str(number_of_planet).isdecimal() and int(number_of_planet) > len(
            objects) - 2) and number_of_planet is not False:
        writing("Введите другой номер", 300, 350, 32)

    elif number_of_planet is not None and number_of_planet is not False:
        painting_graphics(objects[int(number_of_planet) + 1])
        number_of_planet = False
        visualising = 0
        start = 1

    return number_of_planet, visualising, start


def main():
    """
    Главная функция главного модуля. Отвечает за всё.
    """
    pygame.init()
    loaded_file = "one_satellite.txt"  # Файл, который будет загружен изначально.
    physical_time = 0  # Физическое время, прошедшее со старта моделирования.
    start = 0  # == 1, если моделирование запущено; == 0, если моделирование остановлено;
    loading_file = 0  # == 1, если нажата кнопка load file; == 0, если пользователь ввел новый файл и  нажал Enter.
    loading_is_over = 0  # == 1, если пользователь ввел название нового файла; == 0, когда введенные данные обработаны.
    text_filename = "_"  # переменная, в которой хранится введенный текст для смены файла.
    visualising = 0  # == 1, если нажата кнопка graphics; ==0, если пользователь выбрал обьект для постройки графика.
    number_of_planet = False  # номер планеты, для которой необходимо вывести график

    finished = False

    start_button = Button(0, 600, 100, 100, "start")
    pause_button = Button(0, 700, 100, 100, "pause")
    timer = Timer(100, 600, 200, 200, "time:")
    load_from_file_button = Button(300, 600, 150, 200, "load_from_file")
    save_file_button = Button(450, 600, 150, 100, "save_file")
    graphic_button = Button(450, 700, 150, 100, "Graphics")
    buttons = [start_button, pause_button, load_from_file_button, save_file_button,
               graphic_button]  # массив с нажимаемыми кнопками.
    objects = solar_input.read_space_objects_data_from_file(loaded_file)

    max_distance = calculating_max_distance(objects)

    SCREEN.fill(WHITE)
    print('Modelling started!')

    while not finished:  # главный цикл главного модуля
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:  # Проверяет на какую кнопку нажал пользователь
                    button.is_button_pressed(event)
                start, loading_file, visualising = statecheck(start_button, pause_button, load_from_file_button,
                                                              graphic_button, start, loading_file, visualising)
                if save_file_button.pressed is True:
                    solar_input.statistics("stats.txt", objects, physical_time)
            if event.type == pygame.KEYDOWN:
                if loading_file == 0 and visualising == 0:  # если не идет загрузка
                    timer.update(event)
                if loading_file == 1:
                    # если загрузка файла запущена, то нажатые буквы выводятся на экран, записываются в text_filename
                    if event.key == pygame.K_BACKSPACE and len(text_filename) >= 1:  # стирает последний символ
                        text_filename = text_filename[:-1]
                    else:
                        text_filename += event.unicode
                        text_filename = "".join(symbol for symbol in text_filename if not symbol.isdecimal())
                if event.key == pygame.K_RETURN:  # если нажат Enter, то запускается обработка введенного текста.
                    loading_is_over = 1
                if visualising == 1:
                    number_of_planet = event.unicode
        if start == 1:  # выполняется, если моделирование запущено.
            physical_time += timer.set_time_step()
            SCREEN.fill(WHITE)
            writing(str(physical_time), 50, 50)
            for obj in objects:
                model.recalculate_space_objects_positions(objects, timer.set_time_step())
                vis.update_object_position(SCREEN, obj, max_distance)

        if loading_file == 1:  # выполняется после нажатия на кнопку load file
            SCREEN.fill(WHITE)
            writing("Выберите файл для моделирования из доступных:", 300, 100, 24)
            writing("one_satellite.txt", 300, 150, 32)
            writing("solar_system.txt", 300, 200, 32)
            writing("double_star.txt", 300, 250, 32)
            writing(text_filename, 300, 350, 64)
            if loading_is_over == 1:  # запускается после того, как пользователь ввел название нового файла
                splitted_text_filename = text_filename.rsplit()
                objects = solar_input.read_space_objects_data_from_file(str(splitted_text_filename[0]))
                loaded_file = splitted_text_filename[0]
                max_distance = calculating_max_distance(objects)
                text_filename = "_"
                physical_time = 0
                loading_is_over = 0
                loading_file = 0
                start = 1
        if visualising == 1:
            SCREEN.fill(WHITE)
            number_of_planet, visualising, start = visualising_process(objects, loaded_file, number_of_planet)

        for planet in objects:
            if not isinstance(planet, Star):
                save_planet_parameters(planet, physical_time)
        for button in buttons:
            button.draw()
        timer.draw()

        pygame.display.update()

    print('Modelling finished!')


if __name__ == "__main__":
    main()
