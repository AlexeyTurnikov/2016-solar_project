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
                print("Unknown space object")
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
    r, color, m, x, y, vx, vy = int(line.split()[1]), line.split()[2], int(line.split()[3]), int(line.split()[4]), \
                                int(line.split()[5]), int(line.split()[6]), int(line.split()[7])
    star.set_r(r)
    star.set_color(color)
    star.set_m(m)
    star.set_x(x)
    star.set_y(y)
    star.set_vx(vx)
    star.set_vy(vy)


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
    r, color, m, x, y, vx, vy = int(line.split()[1]), line.split()[2], int(line.split()[3]), int(line.split()[4]), \
                                int(line.split()[5]), int(line.split()[6]), int(line.split()[7])
    planet.set_r(r)
    planet.set_color(color)
    planet.set_m(m)
    planet.set_x(x)
    planet.set_y(y)
    planet.set_vx(vx)
    planet.set_vy(vy)


def write_space_objects_data_to_file(output_filename, space_objects):
    """
    saves the space objects data in the file. output file has the next structure:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>,
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>.
    :param output_filename: the name of output file
    :param space_objects: the list of the objects parameters of which we write to the file

    """
    with open(output_filename, 'w') as out_file:
        line = []
        for obj in space_objects:
            print(out_file, "%s %d %s %f" % ('1', 2, '3', 4.5))
            if obj.type == "star":
                line.append("Star")
            elif obj.type == "planet":
                line.append("Planet")
            line.append(obj.r)
            line.append(obj.color)
            line.append(obj.m)
            line.append(obj.x)
            line.append(obj.y)
            line.append(obj.vx)
            line.append(obj.vy)
            out_file.write(
                line[0] + " " + line[1] + " " + line[2] + " " + line[3] + " " + line[4] + " " + line[5] + " " + line[
                    6] + " " + line[7] + "\n")


# FIXME: хорошо бы ещё сделать функцию, сохранающую статистику в заданный файл...

if __name__ == "__main__":
    print("This module is not for direct call!")
