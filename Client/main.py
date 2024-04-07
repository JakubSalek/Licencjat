import pygame as pg
from Client import Client
from MainMenu import main_menu
import SETTINGS as S

if __name__ == "__main__":
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode(S.WINDOW_SIZE)
    pg.display.set_caption('Gold & Treasures!')
    
    client = Client()
    main_menu(screen, clock, client)


