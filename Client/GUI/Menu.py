import sys
import pygame as pg

class Menu:
    def __init__(self, gui):
        self.reinitialize = False
        self.gui = gui

    def run(self):
        pass

    def draw(self):
        pass

    def reinitialize_menu(self):
        pass
    
    def check_server(self):
        pass

    def close_program(self):
        if self.gui.client.is_running:
            self.gui.client.send_disconnect()
        pg.quit()
        sys.exit()