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
                parse_object_parameters(line, star)
                objects.append(star)
            elif object_type == "planet":
                planet = Planet()
                parse_object_parameters(line, planet)
                objects.append(planet)
            else:
                print("unknown space object")
    return objects


def parse_object_parameters(line, obj):
    """
    reads the object data from the line. input line should have this format:
    Object <radius in pixels> <color> <mass> <x> <y> <vx> <vy>,
    where (x, y) — coordinates of a star, (vx, vy) — velocity.

    the example of a line:
    Star 10 red 1000 1 2 3 4
    :param line: line with the object description
    :param obj: the object from class object which we give parameters
    """
    r, color, m, x, y, vx, vy = line.split()[1], str(line.split()[2]), line.split()[3], line.split()[4], line.split()[
        5], line.split()[6], line.split()[7]

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
    obj.set_r(parameters[0])
    obj.set_color(color)
    obj.set_m(parameters[1])
    obj.set_x(parameters[2])
    obj.set_y(parameters[3])
    obj.set_vx(parameters[4])
    obj.set_vy(parameters[5])


def statistics(output_filename, space_objects, time):
    """
    when needed saves parameters of each object in a file which has the next structure:
    Star <radius in pixels> <color> <mass> <x> <y> <Vx> <Vy>,
    Planet <radius in pixels> <color> <mass> <x> <y> <Vx> <Vy>.
    :param output_filename: the name of output file
    :param space_objects: the list of the objects parameters of which we write to the file
    :param time: time estimated for the moment when user asks for saving parameters to the file
    """
    count = 0
    with open(output_filename, "w") as out_file:
        for obj in space_objects:
            if obj.type == "planet":
                print(f"{count} {time} {obj.type} {obj.x} {obj.y} {obj.vx} {obj.vy}", file=out_file)
                line = str(count) + " " + str(obj.get_distance_massive()) + " " + str(obj.get_v_massive()) + "\n"
                out_file.write(line)
            count += 1


if __name__ == "__main__":
    print("This module is not for direct call!")
