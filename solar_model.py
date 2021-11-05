# coding: utf-8
# license: GPLv3

gravitational_constant = 6.67408E-11


def calculate_force(body, space_objects):
    """
    calculates force with which objects affects the body.
    :param body: object, force on which we calculate
    :param space_objects: objects which affect the body
    """
    body.fx = body.fy = 0
    for obj in space_objects:
        if body == obj:
            continue  # body don't affect itself with gravity force
        r = ((body.x - obj.x) ** 2 + (body.y - obj.y) ** 2) ** 0.5
        body.fx += gravitational_constant * body.m * obj.m * (obj.x - body.x) / r ** 3
        body.fy += gravitational_constant * body.m * obj.m * (obj.y - body.y) / r ** 3


def move_space_object(body, dt):
    """
    moves the body using the force affecting the body.
    :param body: body to be moved
    :param dt: time step
    """
    ax = body.Fx / body.m
    body.vx += ax * dt
    body.x += body.vx * dt
    ay = body.Fy / body.m
    body.vy += ay * dt
    body.y += body.vy * dt
    # FIX ME: not sure if this works


def recalculate_space_objects_positions(space_objects, dt):
    """
    recalculates space objects coordinates
    :param space_objects: the list of objects, for which we recalculate coordinates.
    :param dt: time step
    """
    for body in space_objects:
        calculate_force(body, space_objects)
    for body in space_objects:
        move_space_object(body, dt)


if __name__ == "__main__":
    print("This module is not for direct call!")
