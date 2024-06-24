from GUI.UIComponents.TextFunctions import draw_text
from GUI.UIComponents.InputBox import InputBox
from GUI.UIComponents.Button import Button
from GUI.Menu import Menu
from GUI.SettingsMenu import SettingsMenu
from GUI.HowToMenu import HowToMenu
from GUI.ChooseTableMenu import ChooseTableMenu
import pygame as pg
import SETTINGS as S

class MainMenu(Menu):
    def __init__(self, client, queue, clock, screen):
        super().__init__(client, queue, clock, screen)

        # Zmienne do przycisków
        buttons_width = S.SCREEN_WIDTH/2
        buttons_height = S.SCREEN_HEIGHT/12
        first_pos_x = S.SCREEN_WIDTH/4
        first_pos_y = S.SCREEN_HEIGHT/4 + buttons_height
        buttons_padding = buttons_height * 1.5

        # Przyciski menu
        self.__play_button = Button(first_pos_x, first_pos_y, buttons_width,
                                    buttons_height, "Online Game", self._button_font)
        self.__settings_button = Button(first_pos_x, first_pos_y + buttons_padding, buttons_width,
                                        buttons_height, "Settings", self._button_font)
        self.__how_to_button = Button(first_pos_x, first_pos_y + buttons_padding * 2, buttons_width,
                                      buttons_height, "How to play", self._button_font)
        self.__quit_button = Button(first_pos_x, first_pos_y + buttons_padding * 3, buttons_width,
                                    buttons_height, "Quit", self._button_font)

        # Zmienne do pola na wpisywanie
        ibox_x = S.SCREEN_WIDTH * 3 / 5
        ibox_y = S.SCREEN_HEIGHT * 11 / 12
        ibox_width = S.SCREEN_WIDTH * 2 / 5 - 10
        ibox_height = self._ibox_font.size("j")[1] * 1.5
        self.__ibox = InputBox(ibox_x, ibox_y, ibox_width, ibox_height)

        self.__how_to_menu = HowToMenu(client, queue, clock, screen)
        self.__settings_menu = SettingsMenu(client, queue, clock, screen)
        self.__choose_table_menu = ChooseTableMenu(client, queue, clock, screen)

        self.__menus = [self.__how_to_menu, self.__choose_table_menu]

        self.__reinitialize = False

        self.run()

    def run(self):
        while True:
            self.reinitialize_menu() if self.__reinitialize else None

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close_program()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.__play_button.check_click(event.pos):
                            if not self.__ibox.is_empty() and self.__ibox.get_text() != "Can't connect to the server!":
                                self._client.set_nickname(self.__ibox.get_text())
                                connect = self._client.connect()
                                if connect == 0 or connect == 1:
                                    self.__ibox.set_locked(True)
                                    self.__choose_table_menu.run()
                                else:
                                    self.__ibox.set_color(S.IBOX_FAILURE_COLOR)
                                    self.__ibox.set_text("Can't connect to the server!")
                            else:
                                self.__ibox.set_color(S.IBOX_FAILURE_COLOR)
                                self.__ibox.set_text("")
                        elif self.__settings_button.check_click(event.pos):
                            self.__reinitialize = self.__settings_menu.run()
                        elif self.__how_to_button.check_click(event.pos):
                            self.__how_to_menu.run()
                        elif self.__quit_button.check_click(event.pos):
                            self.close_program()
                        elif self.__ibox.check_click(event.pos) and not self.__ibox.get_locked():
                            self.__ibox.set_active(True)
                            self.__ibox.set_color(S.IBOX_ACTIVE_COLOR)
                            if self.__ibox.get_text == "Can't connect to the server!":
                                self.__ibox.set_text("")
                        else:
                            self.__ibox.set_active(False)
                            self.__ibox.set_color(S.IBOX_INACTIVE_COLOR)
                elif event.type == pg.KEYDOWN:
                    if self.__ibox.get_active() and not self.__ibox.get_locked():
                        if event.key == pg.K_BACKSPACE:
                            self.__ibox.set_text(self.__ibox.get_text()[:-1])
                        else:
                            if len(self.__ibox.get_text()) < 16:
                                if event.unicode and not self.__ibox.check_key(event.key):
                                    self.__ibox.set_text(self.__ibox.get_text() + event.unicode)
        
            self.draw()
            self.check_server()

    def draw(self):
        # Rysowanie menu
        self._screen.fill(S.BG_COLOR)

        # Rysowanie tytułu
        draw_text(self._screen, "Gold & Treasures", S.YELLOW, S.SCREEN_WIDTH/2,
                  S.SCREEN_HEIGHT/8, self._title_font, True)
        
        # Rysowanie przycisków
        self.__play_button.draw(self._screen)
        self.__settings_button.draw(self._screen)
        self.__quit_button.draw(self._screen)
        self.__how_to_button.draw(self._screen)

        # Rysowanie pola do wpisywania
        self.__ibox.draw(self._screen, "Nickname:", self._text_font, self._ibox_font)

        # Odświeżenie ekranu
        pg.display.flip()
        self._clock.tick(S.FPS)

        # Sprawdzenie najechania myszką
        mouse_pos = pg.mouse.get_pos()
        self.__play_button.check_hover(mouse_pos)
        self.__settings_button.check_hover(mouse_pos)
        self.__quit_button.check_hover(mouse_pos)
        self.__how_to_button.check_hover(mouse_pos)


    def reinitialize_menu(self):
        super().reinitialize_menu()
        # Zmienne do przycisków
        buttons_width = S.SCREEN_WIDTH/2
        buttons_height = S.SCREEN_HEIGHT/12
        first_pos_x = S.SCREEN_WIDTH/4
        first_pos_y = S.SCREEN_HEIGHT/4 + buttons_height
        buttons_padding = buttons_height * 1.5

        # Przyciski menu
        self.__play_button = Button(first_pos_x, first_pos_y, buttons_width,
                                    buttons_height, "Online Game", self._button_font)
        self.__settings_button = Button(first_pos_x, first_pos_y + buttons_padding, buttons_width,
                                        buttons_height, "Settings", self._button_font)
        self.__how_to_button = Button(first_pos_x, first_pos_y + buttons_padding * 2, buttons_width,
                                      buttons_height, "How to play", self._button_font)
        self.__quit_button = Button(first_pos_x, first_pos_y + buttons_padding * 3, buttons_width,
                                    buttons_height, "Quit", self._button_font)

        # Zmienne do pola na wpisywanie
        ibox_x = S.SCREEN_WIDTH * 3 / 5
        ibox_y = S.SCREEN_HEIGHT * 11 / 12
        ibox_width = S.SCREEN_WIDTH * 2 / 5 - 10
        ibox_height = self._ibox_font.size("j")[1] * 1.5
        self.__ibox = InputBox(ibox_x, ibox_y, ibox_width, ibox_height)

        for menu in self.__menus:
            menu.reinitialize_menu()

        self.__reinitialize = False


    def check_server(self):
        while not self._message_queue.empty():
            message = self._message_queue.get_nowait()
            print(f"Unhandled message \"{message}\"") if S.DEBUG else None

    def close_program(self):
        return super().close_program()