import pygame
from Client import Client
from MainMenu import main_menu
import SETTINGS as S

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(S.WINDOW_SIZE)
    pygame.display.set_caption('Gold & Treasures!')
    
    client = Client()
    main_menu(screen, clock, client)


