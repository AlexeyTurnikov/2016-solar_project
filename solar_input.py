# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet


def read_space_objects_data_from_file(input_filename):
    """
    reads the space objects data from file, creates these objects and calls the creation of their graphic image.
    :param input_filename: the name of input file
    :return: a group of objects in one list with parameters from file
    """
    objects = []
    with open(input_filename) as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # pass the empty or comment line
            object_type = line.split()[0].lower()
            if object_type == "star":
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            elif object_type == "planet":
                planet = Planet()
                parse_planet_parameters(line, planet)
                objects.append(planet)
            else:
                print("unknown space object")
    return objects


def parse_star_parameters(line, star):
    """
    reads the star data from the line. input line should have this format:
    Star <radius in pixels> <color> <mass> <x> <y> <vx> <vy>,
    where (x, y) — coordinates of a star, (vx, vy) — velocity.

    the example of a line:
    Star 10 red 1000 1 2 3 4
    :param line: line with the star description
    :param star: the object from class Star which we give parameters
    """
    r, color, m, x, y, vx, vy = line.split()[1], str(line.split()[2]), line.split()[3], line.split()[4], \
                                line.split()[5], line.split()[6], line.split()[7]

    parameters = [r, m, x, y, vx, vy]
    number_of_parameter = -1
    for parameter in parameters:
        number_of_parameter += 1
        if isinstance(parameter, str) is True:
            parameter = parameter.split("E")
            if len(parameter) > 1:
                parameter[0] = float(parameter[0]) * 10 ** float(parameter[1])
                parameters[number_of_parameter] = int(parameter[0])
            else:
                parameters[number_of_parameter] = int(parameter[0])
    star.set_r(parameters[0])
    star.set_color(color)
    star.set_m(parameters[1])
    star.set_x(parameters[2])
    star.set_y(parameters[3])
    star.set_vx(parameters[4])
    star.set_vy(parameters[5])


def parse_planet_parameters(line, planet):
    """
    reads the planet data from the line. input line should have this format:
    Star <radius in pixels> <color> <mass> <x> <y> <vx> <vy>,
    where (x, y) — coordinates of a planet, (vx, vy) — velocity.

    the example of a line:
    Planet 10 red 1000 1 2 3 4
    :param line: line with the planet description
    :param planet: the object from class Planet which we give parameters
    """
    r, color, m, x, y, vx, vy = line.split()[1], str(line.split()[2]), line.split()[3], line.split()[4], \
                                line.split()[5], line.split()[6], line.split()[7]

    parameters = [r, m, x, y, vx, vy]
    number_of_parameter = -1
    for parameter in parameters:
        number_of_parameter += 1
        if isinstance(parameter, str) is True:
            parameter = parameter.split("E")
            if len(parameter) > 1:
                parameter[0] = float(parameter[0]) * 10 ** float(parameter[1])
                parameters[number_of_parameter] = int(parameter[0])
            else:
                parameters[number_of_parameter] = int(parameter[0])
    planet.set_r(parameters[0])
    planet.set_color(color)
    planet.set_m(parameters[1])
    planet.set_x(parameters[2])
    planet.set_y(parameters[3])
    planet.set_vx(parameters[4])
    planet.set_vy(parameters[5])


def statistics(output_filename, space_objects, time):
    """
    when needed saves parameters of each object in a file which has the next structure:
    Star <radius in pixels> <color> <mass> <x> <y> <Vx> <Vy>,
    Planet <radius in pixels> <color> <mass> <x> <y> <Vx> <Vy>.
    :param output_filename: the name of output file
    :param space_objects: the list of the objects parameters of which we write to the file
    :param time: time estimated for the moment when user asks for saving parameters to the file
    """
    with open(output_filename, "w") as out_file:
        for obj in space_objects:
            print(f"{obj.type} {obj.r} {obj.color} {obj.m} {obj.x} {obj.y} {obj.vx} {obj.vy}", file=out_file)


if __name__ == "__main__":
    print("This module is not for direct call!")
