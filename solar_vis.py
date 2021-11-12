# coding: utf-8
# license: GPLv3
import pygame

"""
visualisation module.
functions creating graphic objects and moving them on the screen, get physical coordinates.
"""

pygame.init()

header_font = pygame.font.SysFont('Arial', 16)
""" font used in header"""
window_width = 600
window_height = 600

"""
adjusting screen coordinates in relation to physical coordinates. 
type: float
units: number of pixels per 1 meter
"""


def calculate_scale_factor(max_distance):
    """
    calculates scaling factor using given length.
    :param max_distance: given length
    :return: scaling parameter
    """
    scaling = 0.4 * min(window_height, window_width) / max_distance
    return scaling


def scale_coord(body, coord, scale_factor, x_or_y):
    """
    calculates screen coordinate using physical coordinate. if coordinate is out of screen, returns it as it is.

    :param body: body, for which we scale coordinates
    :param coord: initial body coordinate in physical system
    :param scale_factor: scaling parameter
    :param x_or_y: if there's x coordinate given, == 1. if y coordinate given, == 0
    :returns: position where the body needs to appear
    """
    if x_or_y == 0:
        position_corrector = window_width
    else:
        position_corrector = window_height
    r = body.get_r()
    position = - int(coord * scale_factor) + position_corrector // 2
    if position >= position_corrector - r:
        position = position_corrector + r
    if position <= r:
        position = -2 * r
    return position


def update_object_position(space, body, max_distance):
    """
    creates object on screen.

    :param space: surface where we need to draw body
    :param body: body which is needed to be drawn
    :param max_distance: length used to calculate scaling parameter
    """
    scale_factor = calculate_scale_factor(max_distance)
    x = scale_coord(body, body.get_x(), scale_factor, 1)
    y = scale_coord(body, body.get_y(), scale_factor, 0)
    r = body.get_r()
    color = body.get_color()
    pygame.draw.circle(space, color, (x, y), r)


def update_system_name(space, system_name):
    """
    creates a text on screen with the name of the system of the bodies.

    :param space: surface to draw on
    :param system_name: the name of the system of bodies
    """
    words = header_font.render(system_name, True, (0, 0, 0))
    place = words.get_rect(center=(30, 80))
    space.blit(words, place)


if __name__ == "__main__":
    print("This module is not for direct call!")
