import pygame as pg
import threading
from GUI.MainMenu import MainMenu
import SETTINGS as S

class GUI(threading.Thread):
    def __init__(self, client, queue):
        # Do threadingu
        super().__init__()

        # Inicjalizacja wszystkich zmiennych pygame
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(S.WINDOW_SIZE)
        pg.display.set_caption('Gold & Treasures!')

        # Inicjalizacja wspólnych elementów interfejsu
        self.text_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.03))
        self.ibox_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.02))
        self.title_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.1))
        self.button_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.04))


        # Kolejka wiadomości od serwera
        self.client = client
        self.message_queue = queue

        # Rozpoczęcie wyświetlania menu
        self.menu = MainMenu(self)

    def reinitialize_menu(self):
        self.text_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.03))
        self.title_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.1))
        self.button_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.04))
        