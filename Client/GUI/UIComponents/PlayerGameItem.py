from GUI.UIComponents.TextFunctions import draw_text
import pygame as pg
import SETTINGS as S

class PlayerGameItem:
    def __init__(self, player, font, width, height):
        self.__swidth = width
        self.__sheight = height
        self.__surface = pg.Surface((width, height))
        self.__player = player
        self.__font = font
        self.__rect = self.__surface.get_rect()

    def draw(self):
        self.__surface.fill(self.__player.get_color())
        draw_text(self.__surface, self.__player.get_nickname(), S.BLACK,
                  self.__swidth//2, self.__sheight * 0.2, self.__font, True)
        draw_text(self.__surface, f"Gold: {self.__player.get_gold()}", S.BLACK,
                  self.__swidth//2, self.__sheight * 0.45, self.__font, True)
        draw_text(self.__surface, f"Goal: {self.__player.get_progress()+1}/{S.TILE_COUNT}",
                  S.BLACK, self.__swidth//2, self.__sheight * 0.75, self.__font, True)

    def get_surface(self):
        return self.__surface
    
    def get_rect(self):
        return self.__rect
    
    def set_rect(self, rect):
        self.__rect = rect