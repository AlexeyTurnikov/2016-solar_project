# coding: utf-8
# license: GPLv3


class Star:
    """Тип данных, описывающий звезду.
    Содержит массу, координаты, скорость звезды,
    а также визуальный радиус звезды в пикселах и её цвет.
    """

    type = "star"
    """Признак объекта звезды"""

    m = 0
    """Масса звезды"""

    x = 0
    """Координата по оси **x**"""

    y = 0
    """Координата по оси **y**"""

    vx = 0
    """Скорость по оси **x**"""

    vy = 0
    """Скорость по оси **y**"""

    fx = 0
    """Сила по оси **x**"""

    fy = 0
    """Сила по оси **y**"""

    r = 5
    """Радиус звезды"""

    color = "red"
    """Цвет звезды"""

    image = None
    """Изображение звезды"""

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

    def get_image(self):
        return self.image

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

    def set_image(self, boolean: bool):
        self.image = boolean


class Planet:
    """Тип данных, описывающий планету.
    Содержит массу, координаты, скорость планеты,
    а также визуальный радиус планеты в пикселах и её цвет
    """

    type = "planet"
    """Признак объекта планеты"""

    m = 0
    """Масса планеты"""

    x = 0
    """Координата по оси **x**"""

    y = 0
    """Координата по оси **y**"""

    vx = 0
    """Скорость по оси **x**"""

    vy = 0
    """Скорость по оси **y**"""

    fx = 0
    """Сила по оси **x**"""

    fy = 0
    """Сила по оси **y**"""

    r = 5
    """Радиус планеты"""

    color = "green"
    """Цвет планеты"""

    image = None
    """Изображение планеты"""

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

    def get_image(self):
        return self.image

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

    def set_image(self, boolean: bool):
        self.image = boolean
