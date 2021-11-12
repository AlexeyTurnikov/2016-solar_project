# coding: utf-8
# license: GPLv3

import pygame
import solar_vis as vis
import solar_model as model
import solar_input
from solar_objects import Star
import matplotlib.pyplot as plt

HEIGHT = 800  # screen height

WIDTH = 600  # screen width

FPS = 30  # number of frames per second

# colors
GREY = (128, 128, 128)
RED = (200, 50, 100)
WHITE = (255, 255, 200)
BLACK = (0, 0, 0)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def calculating_max_distance(objects):
    """
    calculates the max distance between two objects.
    """
    distances = []
    for obj in objects:
        distances.append(max(abs(obj.get_x()), abs(obj.get_y())))
    return max(distances)


def writing(text: str, xcenter, ycenter, font_size=16):
    """
    writes text on screen
    :param text: text to appear on screen
    :param xcenter: x coordinate of center
    :param ycenter: y coordinate of center
    :param font_size: size of the font, which is standart Arial
    """
    font = pygame.font.SysFont('Arial', font_size)
    words = font.render(text, True, (0, 0, 0))
    place = words.get_rect(center=(xcenter, ycenter))
    SCREEN.blit(words, place)


def statecheck(starting, pausing, loading, visualise, start, loading_file, visualising):
    """
    checks which button is pressed by user.
    :param starting: button for the start of modelling
    :param pausing: button for the modelling to pause
    :param loading: button for loading a new file
    :param visualise: button for displaying the graphics
    :param start: parameter using to get info if modelling has started
    :param loading_file: parameter using to get info if loading of a new file has started
    :param visualising: parameter using to get info if graphic was started drawing
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
    function which saves data about the velocity and distance to star of an object every 50000 years.

    :param planet: planet for which we save data
    :param physical_time: physical time after the start of modelling
    """
    i = 1
    if physical_time - i * 500000 > 0:
        planet.append_v_massive((planet.get_vx() ** 2 + planet.get_vy() ** 2) ** 0.5)
        planet.append_distance_massive((planet.get_x() ** 2 + planet.get_y() ** 2) ** 0.5)
        i += 1


def painting_graphics(planet):
    """
    function working with lists of velocities and coordinates and drawing graphics. Graph is drawn using the last 100
    positions (or less).

    :param planet: planet, for which we draw graphics
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
    function responsible for a menu of the choice of a planet for which user wants to create graphic. starts the
    drawing of it.

    :param objects: list with all the objects in a model
    :param loaded_file: file which is currently modelling
    :param number_of_planet: number of a planet for which user wants to get graphic
    :returns: number_of_planet, visualising, start
    """
    visualising = 1
    start = 0
    names = ["Mercury", "Venus", "Earth", "Mars", "Jupyter", "Saturn", "Uranus", "Neptune"]
    writing("Enter the number of a chosen planet: ", 300, 100)
    if loaded_file == "solar_system.txt":
        for i in range(0, len(objects) - 1):
            writing(names[i] + " [ " + str(i) + " ] ", 300, 125 + i * 25)
    if loaded_file == "double_star.txt":
        writing("None of the objects", 300, 125)
        writing("is a planet", 300, 150)
        if number_of_planet is not False:
            number_of_planet = False
            visualising = 0
            start = 1
    if loaded_file == "one_satellite.txt":
        writing("planet [0]", 300, 125)
    if (not str(number_of_planet).isdecimal() or str(number_of_planet).isdecimal() and int(number_of_planet) > len(
            objects) - 2) and number_of_planet is not False:
        writing("Enter another number: ", 300, 350, 32)

    elif number_of_planet is not None and number_of_planet is not False:
        painting_graphics(objects[int(number_of_planet) + 1])
        number_of_planet = False
        visualising = 0
        start = 1

    return number_of_planet, visualising, start


def loading_process(objects, loaded_file, max_distance, text_filename, physical_time, loading_is_over):
    """
    responses for a new file loading.
    :param objects: objects of a modelling system
    :param loaded_file: file which is loaded at this particular moment
    :param max_distance: maximal distance between planet and a star
    :param text_filename: name of file which need to be loaded. gets from a keyboard
    :param physical_time: physical time after the start of modelling
    :param loading_is_over: == 1, if user entered the name of a new file; == 0, if the entered data is processed
    :returns:  objects, loaded_file, max_distance, text_filename, physical_time, loading_is_over, loading_file, start
    """

    start = 0
    loading_file = 1
    writing("Choose a file for modelling:", 300, 100, 24)
    writing("one_satellite.txt", 300, 150, 32)
    writing("solar_system.txt", 300, 200, 32)
    writing("double_star.txt", 300, 250, 32)
    writing(text_filename, 300, 350, 64)
    if loading_is_over == 1:  # starts after a user entered the name of a file
        splitted_text_filename = text_filename.rsplit()
        objects = solar_input.read_space_objects_data_from_file(str(splitted_text_filename[0]))
        loaded_file = splitted_text_filename[0]
        max_distance = calculating_max_distance(objects)
        text_filename = "_"
        physical_time = 0
        loading_is_over = 0
        loading_file = 0
        start = 1
    return objects, loaded_file, max_distance, text_filename, physical_time, loading_is_over, loading_file, start


class Button:
    """
    class of buttons on the screen.
    """

    def __init__(self, x, y, length, width, text: str, ):
        """
        constructor of button class.
        :param x: horizontal coordinate of a button
        :param y: vertical coordinate of a button
        :param length: length of a button
        :param width: width of a button
        :param text: text displayed on a button
        """
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.text = text
        self.color = GREY
        self.pressed = False
        self.timer = 0

    def draw(self):
        """
        function drawing the button on a screen.
        """
        if self.pressed is True:  # pressed button turns red
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
        checks if button is pressed.
        """
        if self.x < event.pos[0] < self.x + self.length and self.y < event.pos[1] < self.y + self.width:
            self.pressed = True
            self.timer = 1


class Timer(Button):
    """
    inherit button class with feature of inserting time.
    """

    def __init__(self, x, y, length, width, text: str):
        """
        constructor of timer class. parameters are identical to button's.
        """
        super().__init__(x, y, length, width, text)
        self.time = "1"

    def draw(self):
        """
        draws a timer button with step of time on it.
        """
        super().draw()
        writing(self.time, self.x + self.length / 2, self.y + 2 * self.width / 3)

    def update(self, event):
        """
        function, checking what number does the user prints on the keyboard and updating the text wrote on the timer
        button.
        """
        if event.key == pygame.K_BACKSPACE and len(self.time) >= 1:
            self.time = self.time[:-1]
        elif len(self.time) <= 10:
            self.time += event.unicode
            self.time = "".join(symbol for symbol in self.time if symbol.isdecimal())  # проверяет введена ли цифра

    def set_time_step(self):
        """
        returns the time step printed on the keyboard.
        :return: step of time
        """
        if len(self.time) >= 1:
            time_step = int(self.time)
        else:
            time_step = 1
        return time_step


def main():
    """
    main function of the main module.
    """
    pygame.init()
    loaded_file = "one_satellite.txt"  # initial loaded file;
    physical_time = 0  # physical time after the start of modelling;
    start = 0  # == 1, if modelling is running; == 0, if modelling is paused;
    loading_file = 0  # == 1, if load file button is pressed; == 0, if a user printed another file and pressed Enter;
    loading_is_over = 0  # == 1, if the user printed a new file name; == 0, when input data is processed;
    text_filename = "_"  # variable with printed text for the change of a file;
    visualising = 0  # == 1, if graphics button is pressed; ==0, if user had chosen the object to build a graph;
    number_of_planet = False  # number of planet, for which we need to build a graphic.

    finished = False

    start_button = Button(0, 600, 100, 100, "start")
    pause_button = Button(0, 700, 100, 100, "pause")
    timer = Timer(100, 600, 200, 200, "time:")
    load_from_file_button = Button(300, 600, 150, 200, "load_from_file")
    save_file_button = Button(450, 600, 150, 100, "save_file")
    graphic_button = Button(450, 700, 150, 100, "Graphics")
    buttons = [start_button, pause_button, load_from_file_button, save_file_button,
               graphic_button]  # list with possibly pressed buttons
    objects = solar_input.read_space_objects_data_from_file(loaded_file)

    max_distance = calculating_max_distance(objects)

    SCREEN.fill(WHITE)
    print('Modelling started!')

    while not finished:  # the main cycle of the main module
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:  # checks which button is pressed
                    button.is_button_pressed(event)
                start, loading_file, visualising = statecheck(start_button, pause_button, load_from_file_button,
                                                              graphic_button, start, loading_file, visualising)
                if save_file_button.pressed is True:
                    solar_input.statistics("stats.txt", objects, physical_time)

            if event.type == pygame.KEYDOWN:
                if loading_file == 0 and visualising == 0:  # if loading is not in process
                    timer.update(event)

                if loading_file == 1:
                    # if the loading has started, pressed symbols are appearing on the screen and are written to the
                    # filename text
                    if event.key == pygame.K_BACKSPACE and len(text_filename) >= 1:  # стирает последний символ
                        text_filename = text_filename[:-1]
                    else:
                        text_filename += event.unicode
                        text_filename = "".join(symbol for symbol in text_filename if not symbol.isdecimal())

                if event.key == pygame.K_RETURN:  # if Enter is pressed, processing the entered text starts
                    loading_is_over = 1

                if visualising == 1:
                    number_of_planet = event.unicode

        if start == 1:  # if modelling is started
            physical_time += timer.set_time_step()
            SCREEN.fill(WHITE)
            writing(str(physical_time), 50, 50)
            for obj in objects:
                model.recalculate_space_objects_positions(objects, timer.set_time_step())
                vis.update_object_position(SCREEN, obj, max_distance)

        if loading_file == 1:  # if button load file is pressed
            SCREEN.fill(WHITE)
            objects, loaded_file, max_distance, text_filename, physical_time, loading_is_over, loading_file, start = \
                loading_process(objects, loaded_file, max_distance, text_filename, physical_time, loading_is_over)

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
