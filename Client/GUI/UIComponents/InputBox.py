import pygame as pg
import SETTINGS as S
from GUI.UIComponents.TextFunctions import draw_text

class InputBox:
    def __init__(self, x, y, width, height):
        self.__rect = pg.Rect(x, y, width, height)
        self.__color = S.IBOX_INACTIVE_COLOR
        self.__active = False
        self.__locked = False
        self.__text = ''
        self.__bad_keys = [pg.K_ESCAPE, pg.K_RETURN, pg.K_TAB, pg.K_SPACE, pg.K_DELETE, pg.K_KP_ENTER, pg.K_SEMICOLON, pg.K_DOLLAR]

    def draw(self, surface, text, text_font, input_font):
        pg.draw.rect(surface, self.__color, self.__rect, 2)
        pg.draw.rect(surface, S.WHITE, self.__rect.inflate(-4, -4))
        draw_text(surface, text, S.FONT_COLOR, self.__rect.x + 1, self.__rect.y - self.__rect.height * 1.5, text_font, False)
        draw_text(surface, self.__text, S.BLACK, self.__rect.x + 5, self.__rect.y + 5, input_font, False)

    def is_empty(self):
        return len(self.__text) == 0 
    
    def get_text(self):
        return self.__text
    
    def set_text(self, text):
        self.__text = text

    def get_locked(self):
        return self.__locked
    
    def set_locked(self, locked):
        self.__locked = locked

    def get_active(self):
        return self.__active
    
    def set_active(self, active):
        self.__active = active

    def set_color(self, color):
        self.__color = color
    
    def check_click(self, pos):
        return self.__rect.collidepoint(pos)

    def check_key(self, key):
        return key in self.__bad_keys