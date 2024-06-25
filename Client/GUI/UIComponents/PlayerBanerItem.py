from GUI.UIComponents.TextFunctions import draw_text
import SETTINGS as S
import pygame as pg

class PlayerBanerItem:
    def __init__(self, player, font, width, height):
        self.__swidth = width
        self.__sheight = height
        self.__surface = pg.Surface((width, height))
        self.__player = player
        self.__font = font
        self.__rect = self.__surface.get_rect()

    def draw(self):
        self.__surface.fill(S.BETTER_GRAY)
        draw_text(self.__surface, "ID: " + str(self.__player.get_id()), S.FONT_COLOR2,
                   self.__swidth*0.10, self.__sheight*0.5, self.__font, True)
        draw_text(self.__surface, "Name: " + str(self.__player.get_nickname()), S.FONT_COLOR2,
                   self.__swidth*0.5, self.__sheight*0.5, self.__font, True)

    def get_surface(self):
        return self.__surface
    
    def get_rect(self):
        return self.__rect

    def set_rect(self, rect):
        self.__rect = rect