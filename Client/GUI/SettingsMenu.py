from GUI.UIComponents.TextFunctions import draw_text
from GUI.UIComponents.Button import Button
from GUI.UIComponents.Checkbox import Checkbox
from GUI.Menu import Menu
import pygame as pg
import SETTINGS as S

class SettingsMenu(Menu):
    def __init__(self, client, queue, clock, screen):
        super().__init__(client, queue, clock, screen)

        self.__resolution_option = S.RESOLUTION.index(S.WINDOW_SIZE)
        self.__fps_option = S.CAN_FPS.index(S.FPS)

        arrow_width = S.SCREEN_HEIGHT/12
        self.__arrow_height = S.SCREEN_HEIGHT/12

        # Przyciski menu
        self.__back_button = Button(S.SCREEN_WIDTH/5, S.SCREEN_HEIGHT*11/13, S.SCREEN_WIDTH/5,
                                    S.SCREEN_HEIGHT/12, "Back", self._button_font)
        self.__save_button = Button(S.SCREEN_WIDTH*3/5, S.SCREEN_HEIGHT*11/13, S.SCREEN_WIDTH/5,
                                    S.SCREEN_HEIGHT/12, "Save", self._button_font)
        self.__resolution_right_button = Button(S.SCREEN_WIDTH*18/20, S.SCREEN_HEIGHT*8/20, arrow_width,
                                                self.__arrow_height, ">", self._button_font)
        self.__resolution_left_button = Button(S.SCREEN_WIDTH*10/20, S.SCREEN_HEIGHT*8/20, arrow_width,
                                                self.__arrow_height, "<", self._button_font)
        self.__fps_right_button = Button(S.SCREEN_WIDTH*18/20, S.SCREEN_HEIGHT*10/20, arrow_width,
                                        self.__arrow_height, ">", self._button_font)
        self.__fps_left_button = Button(S.SCREEN_WIDTH*10/20, S.SCREEN_HEIGHT*10/20, arrow_width,
                                        self.__arrow_height, "<", self._button_font)
        self.__buttons = [self.__back_button, self.__save_button, self.__fps_left_button,
                          self.__fps_right_button, self.__resolution_left_button, self.__resolution_right_button]

        # Checkbox
        self.__fullscreen_checkbox = Checkbox(self._screen, S.SCREEN_WIDTH*15/20,
                                            S.SCREEN_HEIGHT*6/20, self.__arrow_height, S.GRAY, S.WHITE)
        self.__fullscreen_checkbox.set_checked(S.FULLSCREEN)


    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close_program()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.__back_button.check_click(event.pos):
                            return False
                        elif self.__fullscreen_checkbox.check_click(event.pos):
                            self.__fullscreen_checkbox.toggle()
                        elif self.__resolution_left_button.check_click(event.pos):
                            if self.__resolution_option > 0:
                                self.__resolution_option -= 1
                        elif self.__resolution_right_button.check_click(event.pos):
                            if self.__resolution_option < len(S.RESOLUTION) - 1:
                                self.__resolution_option += 1
                        elif self.__fps_left_button.check_click(event.pos):
                            if self.__fps_option > 0:
                                self.__fps_option -= 1
                        elif self.__fps_right_button.check_click(event.pos):
                            if self.__fps_option < len(S.CAN_FPS) - 1:
                                self.__fps_option += 1
                        elif self.__save_button.check_click(event.pos):
                            S.SCREEN_WIDTH = S.RESOLUTION[self.__resolution_option][0]
                            S.SCREEN_HEIGHT = S.RESOLUTION[self.__resolution_option][1]
                            S.WINDOW_SIZE = (S.SCREEN_WIDTH, S.SCREEN_HEIGHT)
                            S.FPS = S.CAN_FPS[self.__fps_option]
                            S.FULLSCREEN = self.__fullscreen_checkbox.get_checked()
                            
                            flags = pg.FULLSCREEN if S.FULLSCREEN else 0
                            self.__screen = pg.display.set_mode(S.WINDOW_SIZE, flags)
                        
                            self.reinitialize_menu()
                            return True
            self.draw()
            self.check_server()

    def draw(self):
        # Rysowanie menu
        self._screen.fill(S.BG_COLOR)

        # Rysowanie tytułu
        draw_text(self._screen, "Settings", S.FONT_COLOR, S.SCREEN_WIDTH/2,
                  S.SCREEN_HEIGHT/10, self._title_font, True)
        draw_text(self._screen, "Fullscreen", S.FONT_COLOR, S.SCREEN_WIDTH*6/20,
                  S.SCREEN_HEIGHT*6/20+self.__arrow_height/2, self._text_font, True)
        draw_text(self._screen, "Resolution", S.FONT_COLOR, S.SCREEN_WIDTH*6/20,
                  S.SCREEN_HEIGHT*8/20+self.__arrow_height/2, self._text_font, True)
        draw_text(self._screen, "FPS", S.FONT_COLOR, S.SCREEN_WIDTH*6/20,
                  S.SCREEN_HEIGHT*10/20+self.__arrow_height/2, self._text_font, True)
        resolution_text = str(S.RESOLUTION[self.__resolution_option][0]) + "x" + str(S.RESOLUTION[self.__resolution_option][1])
        draw_text(self._screen, resolution_text, S.FONT_COLOR, S.SCREEN_WIDTH*15/20,
                  S.SCREEN_HEIGHT*8/20+self.__arrow_height/2, self._text_font, True)
        draw_text(self._screen, str(S.CAN_FPS[self.__fps_option]), S.FONT_COLOR, S.SCREEN_WIDTH*15/20,
                  S.SCREEN_HEIGHT*10/20+self.__arrow_height/2, self._text_font, True)

        # Rysowanie przycisków
        for button in self.__buttons:
            button.draw(self._screen)

        self.__fullscreen_checkbox.draw()

        # Odświeżenie ekranu
        pg.display.flip()
        self._clock.tick(S.FPS)

        # Sprawdzenie najechania myszką
        mouse_pos = pg.mouse.get_pos()
        for button in self.__buttons:
            button.check_hover(mouse_pos)

    def reinitialize_menu(self):
        self.__resolution_option = S.RESOLUTION.index(S.WINDOW_SIZE)
        self.__fps_option = S.CAN_FPS.index(S.FPS)

        arrow_width = S.SCREEN_HEIGHT/12
        self.__arrow_height = S.SCREEN_HEIGHT/12

        # Przyciski menu
        self.__back_button = Button(S.SCREEN_WIDTH/5, S.SCREEN_HEIGHT*11/13, S.SCREEN_WIDTH/5,
                                    S.SCREEN_HEIGHT/12, "Back", self._button_font)
        self.__save_button = Button(S.SCREEN_WIDTH*3/5, S.SCREEN_HEIGHT*11/13, S.SCREEN_WIDTH/5,
                                    S.SCREEN_HEIGHT/12, "Save", self._button_font)
        self.__resolution_right_button = Button(S.SCREEN_WIDTH*18/20, S.SCREEN_HEIGHT*8/20, arrow_width,
                                                self.__arrow_height, ">", self._button_font)
        self.__resolution_left_button = Button(S.SCREEN_WIDTH*10/20, S.SCREEN_HEIGHT*8/20, arrow_width,
                                                self.__arrow_height, "<", self._button_font)
        self.__fps_right_button = Button(S.SCREEN_WIDTH*18/20, S.SCREEN_HEIGHT*10/20, arrow_width,
                                        self.__arrow_height, ">", self._button_font)
        self.__fps_left_button = Button(S.SCREEN_WIDTH*10/20, S.SCREEN_HEIGHT*10/20, arrow_width,
                                        self.__arrow_height, "<", self._button_font)
        self.__buttons = [self.__back_button, self.__save_button, self.__fps_left_button,
                          self.__fps_right_button, self.__resolution_left_button, self.__resolution_right_button]

        # Checkbox
        self.__fullscreen_checkbox = Checkbox(self._screen, S.SCREEN_WIDTH*15/20,
                                            S.SCREEN_HEIGHT*6/20, self.__arrow_height, S.GRAY, S.WHITE)
        self.__fullscreen_checkbox.set_checked(S.FULLSCREEN)


    def check_server(self):
        while not self._message_queue.empty():
            message = self._message_queue.get_nowait()
            print(f"Unhandled message \"{message}\"") if S.DEBUG else None
            
    def close_program(self):
        return super().close_program()