import pygame as pg
import SETTINGS as S

class TileGameItem:
    def __init__(self, width, height) -> None:
        self.__swidth = width
        self.__sheight = height
        self.__surface = pg.Surface((width, height), pg.SRCALPHA)
        self.__rect = self.__surface.get_rect()
        self.__player_width = self.__swidth // 2
        self.__player_height = self.__sheight // 2
        self.__player_radius = self.__swidth // 6
    
    def draw(self, players):
        self.__surface.fill(S.TILE_COLOR)
        for i, player in enumerate(players):
            posx = (i % 2) * self.__player_width + self.__player_radius + (self.__swidth // 10)
            posy = (i // 2) * self.__player_height + self.__player_radius + (self.__sheight // 14)
            pg.draw.circle(self.__surface, player.get_color(), (posx, posy), self.__player_radius)

    def get_surface(self):
        return self.__surface
    
    def get_rect(self):
        return self.__rect
    
    def set_rect_topleft(self, topleft):
        self.__rect.topleft = topleft