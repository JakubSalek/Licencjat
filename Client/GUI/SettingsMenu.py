from GUI.UIComponents import draw_text, Button, Checkbox
from GUI.Menu import Menu
import pygame as pg
import SETTINGS as S
import sys

class SettingsMenu(Menu):
    def __init__(self, gui):
        super().__init__(gui)
        self.options_changed = False

        self.resolution_option = S.RESOLUTION.index(S.WINDOW_SIZE)
        self.fps_option = S.CAN_FPS.index(S.FPS)

        button_font = self.gui.button_font
        self.arrow_width = S.SCREEN_WIDTH/12
        self.arrow_height = S.SCREEN_HEIGHT/12

        # Przyciski menu
        self.back_button = Button(S.SCREEN_WIDTH/5, S.SCREEN_HEIGHT*11/13, S.SCREEN_WIDTH/5,
                                S.SCREEN_HEIGHT/12, "Back", button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
        self.save_button = Button(S.SCREEN_WIDTH*3/5, S.SCREEN_HEIGHT*11/13, S.SCREEN_WIDTH/5,
                                S.SCREEN_HEIGHT/12, "Save", button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
        self.resolution_right_button = Button(S.SCREEN_WIDTH*18/20, S.SCREEN_HEIGHT*8/20, self.arrow_width,
                                            self.arrow_height, ">", button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
        self.resolution_left_button = Button(S.SCREEN_WIDTH*10/20, S.SCREEN_HEIGHT*8/20, self.arrow_width,
                                            self.arrow_height, "<", button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
        self.fps_right_button = Button(S.SCREEN_WIDTH*18/20, S.SCREEN_HEIGHT*10/20, self.arrow_width,
                                    self.arrow_height, ">", button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
        self.fps_left_button = Button(S.SCREEN_WIDTH*10/20, S.SCREEN_HEIGHT*10/20, self.arrow_width,
                                    self.arrow_height, "<", button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)

        # Checkbox
        self.fullscreen_checkbox = Checkbox(self.gui.screen, S.SCREEN_WIDTH*15/20, S.SCREEN_HEIGHT*6/20, self.arrow_height, S.GRAY, S.WHITE)
        self.fullscreen_checkbox.checked = S.FULLSCREEN

        self.buttons = [self.back_button, self.save_button, self.fps_left_button, self.fps_right_button, self.resolution_left_button, self.resolution_right_button]

    def run(self):
        while True:
            self.reinitialize_menu() if self.reinitialize else None

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close_program()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.back_button.rect.collidepoint(event.pos):
                            return False
                        elif self.fullscreen_checkbox.rect.collidepoint(event.pos):
                            self.fullscreen_checkbox.toggle()
                        elif self.resolution_left_button.rect.collidepoint(event.pos):
                            if self.resolution_option > 0:
                                self.resolution_option -= 1
                        elif self.resolution_right_button.rect.collidepoint(event.pos):
                            if self.resolution_option < len(S.RESOLUTION) - 1:
                                self.resolution_option += 1
                        elif self.fps_left_button.rect.collidepoint(event.pos):
                            if self.fps_option > 0:
                                self.fps_option -= 1
                        elif self.fps_right_button.rect.collidepoint(event.pos):
                            if self.fps_option < len(S.CAN_FPS) - 1:
                                self.fps_option += 1
                        elif self.save_button.rect.collidepoint(event.pos):
                            S.SCREEN_WIDTH = S.RESOLUTION[self.resolution_option][0]
                            S.SCREEN_HEIGHT = S.RESOLUTION[self.resolution_option][1]
                            S.WINDOW_SIZE = (S.SCREEN_WIDTH, S.SCREEN_HEIGHT)
                            S.FPS = S.CAN_FPS[self.fps_option]
                            S.FULLSCREEN = self.fullscreen_checkbox.checked
                            
                            flags = pg.FULLSCREEN if S.FULLSCREEN else 0
                            self.gui.screen = pg.display.set_mode(S.WINDOW_SIZE, flags)
                            
                            self.gui.reinitialize_menu()

                            self.reinitialize = True
                            return True
            self.draw()
            self.check_server()

    def draw(self):
        screen = self.gui.screen
        text_font = self.gui.text_font
        # Rysowanie menu
        screen.fill(S.BG_COLOR)

        # Rysowanie tytułu
        draw_text(screen, "Settings", S.FONT_COLOR, S.SCREEN_WIDTH/2, S.SCREEN_HEIGHT/10, self.gui.title_font, True)
        draw_text(screen, "Fullscreen", S.FONT_COLOR, S.SCREEN_WIDTH*6/20, S.SCREEN_HEIGHT*6/20+self.arrow_height/2, text_font, True)
        draw_text(screen, "Resolution", S.FONT_COLOR, S.SCREEN_WIDTH*6/20, S.SCREEN_HEIGHT*8/20+self.arrow_height/2, text_font, True)
        draw_text(screen, "FPS", S.FONT_COLOR, S.SCREEN_WIDTH*6/20, S.SCREEN_HEIGHT*10/20+self.arrow_height/2, text_font, True)
        resolution_text = str(S.RESOLUTION[self.resolution_option][0]) + "x" + str(S.RESOLUTION[self.resolution_option][1])
        draw_text(screen, resolution_text, S.FONT_COLOR, S.SCREEN_WIDTH*15/20, S.SCREEN_HEIGHT*8/20+self.arrow_height/2, text_font, True)
        draw_text(screen, str(S.CAN_FPS[self.fps_option]), S.FONT_COLOR, S.SCREEN_WIDTH*15/20, S.SCREEN_HEIGHT*10/20+self.arrow_height/2, text_font, True)

        # Rysowanie przycisków
        for button in self.buttons:
            button.draw(screen)

        self.fullscreen_checkbox.draw()

        # Odświeżenie ekranu
        pg.display.flip()
        self.gui.clock.tick(S.FPS)

        # Sprawdzenie najechania myszką
        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.check_hover(mouse_pos)

    def reinitialize_menu(self):
        button_font = self.gui.button_font

        self.arrow_width = S.SCREEN_WIDTH/12
        self.arrow_height = S.SCREEN_HEIGHT/12

        # Przyciski menu
        self.back_button = Button(S.SCREEN_WIDTH/5, S.SCREEN_HEIGHT*11/13, S.SCREEN_WIDTH/5,
                                S.SCREEN_HEIGHT/12, "Back", button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
        self.save_button = Button(S.SCREEN_WIDTH*3/5, S.SCREEN_HEIGHT*11/13, S.SCREEN_WIDTH/5,
                                S.SCREEN_HEIGHT/12, "Save", button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
        self.resolution_right_button = Button(S.SCREEN_WIDTH*18/20, S.SCREEN_HEIGHT*8/20, self.arrow_width,
                                            self.arrow_height, ">", button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
        self.resolution_left_button = Button(S.SCREEN_WIDTH*10/20, S.SCREEN_HEIGHT*8/20, self.arrow_width,
                                            self.arrow_height, "<", button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
        self.fps_right_button = Button(S.SCREEN_WIDTH*18/20, S.SCREEN_HEIGHT*10/20, self.arrow_width,
                                    self.arrow_height, ">", button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
        self.fps_left_button = Button(S.SCREEN_WIDTH*10/20, S.SCREEN_HEIGHT*10/20, self.arrow_width,
                                    self.arrow_height, "<", button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)

        # Checkbox
        self.fullscreen_checkbox = Checkbox(self.gui.screen, S.SCREEN_WIDTH*15/20, S.SCREEN_HEIGHT*6/20, self.arrow_height, S.GRAY, S.WHITE)
        self.fullscreen_checkbox.checked = S.FULLSCREEN

        self.buttons = [self.back_button, self.save_button, self.fps_left_button, self.fps_right_button, self.resolution_left_button, self.resolution_right_button]

        self.reinitialize = False


    def check_server(self):
        while not self.gui.message_queue.empty():
            message = self.gui.message_queue.get_nowait()
            
    def close_program(self):
        return super().close_program()