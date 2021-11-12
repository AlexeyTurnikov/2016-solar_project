# coding: utf-8
# license: GPLv3

class Star:
    """
    data type describing a star.
    includes mass, coordinates, velocity of a star, visual radius of a star and its color.
    """

    type = "star"
    """ attribute of a star object """

    m = 0
    """ star mass """

    x = 0
    """ x coordinate """

    y = 0
    """ y coordinate """

    vx = 0
    """ x velocity component """

    vy = 0
    """ y velocity component """

    fx = 0
    """ x force component """

    fy = 0
    """ y force component """

    r = 5
    """ radius of a star """

    color = "red"
    """ color of a star """

    """
    get functions: return one of star's parameters.
    """

    def get_type(self):
        return self.type

    def get_m(self):
        return self.m

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_vx(self):
        return self.vx

    def get_vy(self):
        return self.vy

    def get_fx(self):
        return self.fx

    def get_fy(self):
        return self.fy

    def get_r(self):
        return self.r

    def get_color(self):
        return self.color

    """
    set functions: set one of star's parameters.
    """

    def set_type(self, style: str):
        self.type = style

    def set_m(self, m):
        self.m = m

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_vx(self, vx):
        self.vx = vx

    def set_vy(self, vy):
        self.vy = vy

    def set_fx(self, fx):
        self.fx = fx

    def set_fy(self, fy):
        self.fy = fy

    def set_r(self, r):
        self.r = r

    def set_color(self, color: str):
        self.color = color


class Planet:
    """
    data type describing a planet.
    includes mass, coordinates, velocity of a star, visual radius of a star and its color.
    """

    type = "planet"
    """ attribute of a star object """

    m = 0
    """ planet mass """

    x = 0
    """ x coordinate """

    y = 0
    """ y coordinate """

    vx = 0
    """ x velocity component """

    vy = 0
    """ y velocity component """

    fx = 0
    """ x force component """

    fy = 0
    """ y force component """

    r = 5
    """ radius of a planet"""

    color = "green"
    """ color of a planet """
    v_massive = []
    """ velocities of a planet during time """
    distance_massive = []
    """ distance to the center of the system during time """

    """
    get functions: return one of planet's parameters.
    """

    def get_type(self):
        return self.type

    def get_m(self):
        return self.m

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_vx(self):
        return self.vx

    def get_vy(self):
        return self.vy

    def get_fx(self):
        return self.fx

    def get_fy(self):
        return self.fy

    def get_r(self):
        return self.r

    def get_color(self):
        return self.color

    def get_v_massive(self):
        return self.v_massive

    def get_distance_massive(self):
        return self.distance_massive

    """
    set functions: set one of planet's parameters.
    """

    def set_type(self, style: str):
        self.type = style

    def set_m(self, m):
        self.m = m

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_vx(self, vx):
        self.vx = vx

    def set_vy(self, vy):
        self.vy = vy

    def set_fx(self, fx):
        self.fx = fx

    def set_fy(self, fy):
        self.fy = fy

    def set_r(self, r):
        self.r = r

    def set_color(self, color: str):
        self.color = color

    """
    functions, appending to lists of velocities and coordinates current values.
    """

    def append_v_massive(self, v):
        self.v_massive.append(v)

    def append_distance_massive(self, distance):
        self.distance_massive.append(distance)
