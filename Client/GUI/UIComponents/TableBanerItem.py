from GUI.UIComponents.Button import Button
from GUI.UIComponents.TextFunctions import draw_text
import SETTINGS as S
import pygame as pg

class TableBanerItem:
    def __init__(self, table, font, width, height):
        self.__swidth = width
        self.__sheight = height
        self.__surface = pg.Surface((width, height))
        self.__table = table
        self.__font = font
        self.__rect = pg.Rect(0, 0, 0, 0)
        self.__button = Button(self.__swidth*0.75, self.__sheight*0.25,
                               self.__swidth*0.15, self.__sheight*0.5, "Join", self.__font)
        if self.__table.get_player_count() == "4" or self.__table.get_started():
            self.__button.set_active(False)

    def draw(self):
        self.__surface.fill(S.BETTER_GRAY)
        draw_text(self.__surface, str(self.__table.get_id()), S.FONT_COLOR2,
                  self.__swidth*0.05, self.__sheight*0.5, self.__font, True)
        draw_text(self.__surface, str(self.__table.get_name()), S.FONT_COLOR2,
                  self.__swidth*0.35, self.__sheight*0.5, self.__font, True)
        draw_text(self.__surface, f"{str(self.__table.get_player_count())}/4", S.FONT_COLOR2,
                  self.__swidth*0.65, self.__sheight*0.5, self.__font, True)
        self.__button.draw(self.__surface)

    def get_table(self):
        return self.__table

    def set_rect(self, rect):
        self.__rect = rect

    def get_rect(self):
        return self.__rect

    def get_surface(self):
        return self.__surface

    def check_click(self, pos):
        x, y = pos
        x -= self.__rect.left
        y -= self.__rect.top
        return self.__button.check_click((x, y))
    
    def check_hover(self, pos):
        x, y = pos
        x -= self.__rect.left
        y -= self.__rect.top
        return self.__button.check_hover((x, y))


