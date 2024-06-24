import pygame as pg

class Checkbox:
    def __init__(self, surface, x, y, size=20, color=(200, 200, 200), border_color=(0, 0, 0)):
        self.__surface = surface
        self.__rect = pg.Rect(x, y, size, size)
        self.__color = color
        self.__border_color = border_color
        self.__checked = False

    def draw(self):
        pg.draw.rect(self.__surface, self.__border_color, self.__rect, 2)
        if self.__checked:
            pg.draw.line(self.__surface, self.__border_color, self.__rect.topleft, self.__rect.bottomright, 2)
            pg.draw.line(self.__surface, self.__border_color, self.__rect.topright, self.__rect.bottomleft, 2)

    def toggle(self):
        self.__checked = not self.__checked

    def get_checked(self):
        return self.__checked

    def set_checked(self, checked):
        self.__checked = checked

    def check_click(self, pos):
        return self.__rect.collidepoint(pos)