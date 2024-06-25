import sys
import pygame as pg
import SETTINGS as S

class Menu:
    def __init__(self, client, queue, clock, screen):
        self._clock = clock
        self._screen = screen

        self._ibox_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.02))
        self._text_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.03))
        self._button_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.04))
        self._title_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.1))

        # Kolejka wiadomości od serwera
        self._client = client
        self._message_queue = queue
        
        self._buttons = []
        
    def run(self):
        pass

    def draw(self):
        pass

    def reinitialize_menu(self):
        self._text_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.03))
        self._ibox_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.02))
        self._title_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.1))
        self._button_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.04))
    
    def check_server(self):
        pass

    def close_program(self):
        if self._client.get_is_running():
            self._client.send_disconnect()
        pg.quit()
        sys.exit()