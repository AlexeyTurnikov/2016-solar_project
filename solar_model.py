# coding: utf-8
# license: GPLv3

gravitational_constant = 6.67408E-11


def calculate_force(body, space_objects):
    """
    calculates force with which objects affects the body.
    :param body: object, force on which we calculate
    :param space_objects: objects which affect the body
    """
    x_body = body.get_x()
    y_body = body.get_y()
    m_body = body.get_m()
    fx = body.get_fx()
    fy = body.get_fy()

    for obj in space_objects:
        x_obj = obj.get_x()
        y_obj = obj.get_y()
        m_obj = obj.get_m()
        distance = ((x_body - x_obj) ** 2 + (y_body - y_obj) ** 2) ** 0.5
        if distance != 0:
            fx += gravitational_constant * m_body * m_obj * (x_obj - x_body) / distance ** 3
            fy -= gravitational_constant * m_body * m_obj * (y_obj - y_body) / distance ** 3
        body.set_fx(fx)
        body.set_fy(fy)


def move_space_object(body, dt):
    """
    moves the body using the force affecting the body.
    :param body: body to be moved
    :param dt: time step
    """
    x = body.get_x()
    y = body.get_y()
    vx = body.get_vx()
    vy = body.get_vy()

    ax = body.get_fx() / body.get_m()
    ay = body.fy / body.m
    vx += ax * dt
    x += body.vx * dt
    vy += ay * dt
    y += vy * dt

    body.set_x(x)
    body.set_y(y)
    body.set_vx(vx)
    body.set_vy(vy)
    # FIXME: not sure if this works


def recalculate_space_objects_positions(space_objects, dt):
    """
    recalculates space objects coordinates
    :param space_objects: the list of objects, for which we recalculate coordinates.
    :param dt: time step
    """
    for body in space_objects:
        calculate_force(body, space_objects)
        #    for body in space_objects:
        move_space_object(body, dt)


if __name__ == "__main__":
    print("This module is not for direct call!")
