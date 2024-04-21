import pygame as pg
import sys
from GUI.Menu import Menu
from GUI.SettingsMenu import SettingsMenu
from GUI.HowToMenu import HowToMenu
from GUI.UIComponents import Button, draw_text
import SETTINGS as S

class MainMenu(Menu):
    def __init__(self, gui):
        super().__init__(gui)

        # Zmienne do przycisków
        self.buttons_width = S.SCREEN_WIDTH/2
        self.buttons_height = S.SCREEN_HEIGHT/12
        self.first_pos_x = S.SCREEN_WIDTH/4
        self.first_pos_y = S.SCREEN_HEIGHT/4 + self.buttons_height
        self.buttons_padding = self.buttons_height * 1.5

        # Przyciski menu
        self.play_button = Button(self.first_pos_x, self.first_pos_y, self.buttons_width, self.buttons_height, "Online Game", self.gui.button_font, S.GRAY, S.WHITE)
        self.settings_button = Button(self.first_pos_x, self.first_pos_y + self.buttons_padding, self.buttons_width, self.buttons_height, "Settings", self.gui.button_font, S.GRAY, S.WHITE)
        self.how_to_button = Button(self.first_pos_x, self.first_pos_y + self.buttons_padding * 2, self.buttons_width, self.buttons_height, "How to play", self.gui.button_font, S.GRAY, S.WHITE)
        self.quit_button = Button(self.first_pos_x, self.first_pos_y + self.buttons_padding * 3, self.buttons_width, self.buttons_height, "Quit", self.gui.button_font, S.GRAY, S.WHITE)

        # Zmienne do pola na wpisywanie
        self.ibox_x = S.SCREEN_WIDTH * 3 / 5
        self.ibox_y = S.SCREEN_HEIGHT * 11 / 12
        self.ibox_width = S.SCREEN_WIDTH * 2 / 5 - 10
        self.ibox_height = self.gui.ibox_font.size("j")[1] * 1.5
        self.ibox = pg.Rect(self.ibox_x, self.ibox_y, self.ibox_width, self.ibox_height)
        self.ibox_color_inactive = pg.Color('lightskyblue3')
        self.ibox_color_active = pg.Color('dodgerblue2')
        self.ibox_color_failure = pg.Color(255, 0, 0)
        self.ibox_color = self.ibox_color_inactive
        self.ibox_active = False
        self.ibox_text = ''
        self.bad_keys = [pg.K_ESCAPE, pg.K_RETURN, pg.K_TAB, pg.K_SPACE, pg.K_DELETE, pg.K_KP_ENTER]

        self.how_to_menu = HowToMenu(gui)
        self.settings_menu = SettingsMenu(gui)

        self.menus = [self.how_to_menu]

        self.run()

    def run(self):
        while True:
            self.reinitialize_menu() if self.reinitialize else None

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.play_button.rect.collidepoint(event.pos):
                            if len(self.ibox_text) != 0 and self.ibox_text != "Can't connect to the server!":
                                self.gui.client.nickname = self.ibox_text
                                connect = self.gui.client.connect()
                                if connect == 0:
                                    pass
                                else:
                                    self.ibox_color = self.ibox_color_failure
                                    self.ibox_text = "Can't connect to the server!"
                            else:
                                self.ibox_color = self.ibox_color_failure
                                self.ibox_text = ''
                        elif self.settings_button.rect.collidepoint(event.pos):
                            self.reinitialize = self.settings_menu.run()
                        elif self.how_to_button.rect.collidepoint(event.pos):
                            self.how_to_menu.run()
                        elif self.quit_button.rect.collidepoint(event.pos):
                            pg.quit()
                            sys.exit()
                        elif self.ibox.collidepoint(event.pos):
                            self.ibox_active = True
                            self.ibox_color = self.ibox_color_active
                            if self.ibox_text == "Can't connect to the server!":
                                self.ibox_text = ''
                        else:
                            self.ibox_active = False
                            self.ibox_color = self.ibox_color_inactive
                elif event.type == pg.KEYDOWN:
                    if self.ibox_active:
                        if event.key == pg.K_BACKSPACE:
                            self.ibox_text = self.ibox_text[:-1]
                        else:
                            if len(self.ibox_text) < 16:
                                if event.unicode and event.key not in self.bad_keys:
                                    self.ibox_text += event.unicode
        
            self.draw()

    def draw(self):
        # Pomocnicze zmienne
        screen = self.gui.screen
        text_font = self.gui.text_font
        title_font = self.gui.title_font

        # Rysowanie menu
        screen.fill(S.BLACK)

        # Rysowanie tytułu
        draw_text(screen, "Gold & Treasures", S.YELLOW, S.SCREEN_WIDTH/2, S.SCREEN_HEIGHT/8, title_font, True)
        
        # Rysowanie przycisków
        self.play_button.draw(screen)
        self.settings_button.draw(screen)
        self.quit_button.draw(screen)
        self.how_to_button.draw(screen)

        # Rysowanie pola do wpisywania
        pg.draw.rect(screen, self.ibox_color, self.ibox, 2)
        pg.draw.rect(screen, S.WHITE, self.ibox.inflate(-4, -4))
        draw_text(screen, 'Nickname:', S.WHITE, self.ibox.x + 1, self.ibox.y - self.ibox_height * 1.5, text_font, False)
        draw_text(screen, self.ibox_text, S.BLACK, self.ibox.x + 5, self.ibox.y + 5, self.gui.ibox_font, False)

        # Odświeżenie ekranu
        pg.display.flip()
        self.gui.clock.tick(S.FPS)

        # Sprawdzenie najechania myszką
        mouse_pos = pg.mouse.get_pos()
        self.play_button.check_hover(mouse_pos)
        self.settings_button.check_hover(mouse_pos)
        self.quit_button.check_hover(mouse_pos)
        self.how_to_button.check_hover(mouse_pos)


    def reinitialize_menu(self):
        # Zmienne do przycisków
        self.buttons_width = S.SCREEN_WIDTH/2
        self.buttons_height = S.SCREEN_HEIGHT/12
        self.first_pos_x = S.SCREEN_WIDTH/4
        self.first_pos_y = S.SCREEN_HEIGHT/4 + self.buttons_height
        self.buttons_padding = self.buttons_height * 1.5

        # Przyciski menu
        self.play_button = Button(self.first_pos_x, self.first_pos_y, self.buttons_width, self.buttons_height, "Online Game", self.gui.button_font, S.GRAY, S.WHITE)
        self.settings_button = Button(self.first_pos_x, self.first_pos_y + self.buttons_padding, self.buttons_width, self.buttons_height, "Settings", self.gui.button_font, S.GRAY, S.WHITE)
        self.how_to_button = Button(self.first_pos_x, self.first_pos_y + self.buttons_padding * 2, self.buttons_width, self.buttons_height, "How to play", self.gui.button_font, S.GRAY, S.WHITE)
        self.quit_button = Button(self.first_pos_x, self.first_pos_y + self.buttons_padding * 3, self.buttons_width, self.buttons_height, "Quit", self.gui.button_font, S.GRAY, S.WHITE)

        # Zmienne do pola na wpisywanie
        self.ibox_x = S.SCREEN_WIDTH * 3 / 5
        self.ibox_y = S.SCREEN_HEIGHT * 11 / 12
        self.ibox_width = S.SCREEN_WIDTH * 2 / 5 - 10
        self.ibox_height = self.gui.ibox_font.size("j")[1] * 1.5
        self.ibox = pg.Rect(self.ibox_x, self.ibox_y, self.ibox_width, self.ibox_height)

        for menu in self.menus:
            menu.reinitialize = True

        self.reinitialize = False