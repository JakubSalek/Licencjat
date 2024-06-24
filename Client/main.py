from Client import Client
from GUI.MainMenu import MainMenu
import pygame as pg
import SETTINGS as S
import queue

if __name__ == "__main__":
    # Inicjalizacja kolejki wiadomości
    message_queue = queue.Queue()

    # Inicjalizacja okna pygame
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode(S.WINDOW_SIZE)
    pg.display.set_caption('Gold & Treasures!')

    # Inicjalizacja dwóch głównych wątków
    client = Client(message_queue)
    menu = MainMenu(client, message_queue, clock, screen)
