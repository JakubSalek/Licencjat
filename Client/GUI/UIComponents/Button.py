import SETTINGS as S
import pygame as pg

class Button:
    def __init__(self, x, y, width, height, text, font):
        self.__rect = pg.Rect(x, y, width, height)
        self.__text = text
        self.__font = font
        self.__normal_color = S.BUTTON_COLOR
        self.__hover_color = S.BUTTON_HOVER_COLOR
        self.__hovered = False
        self.__active = True

    def draw(self, surface):
        color = self.__hover_color if self.__hovered else self.__normal_color
        pg.draw.rect(surface, color, self.__rect)
        text_surface = self.__font.render(self.__text, True, S.BLACK)
        text_rect = text_surface.get_rect(center=self.__rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, pos):
        if self.__active:
            self.__hovered = self.__rect.collidepoint(pos)

    def check_click(self, pos):
        if self.__active:
            return self.__rect.collidepoint(pos)
        else:
            return False
    
    def set_active(self, active):
        self.__active = active