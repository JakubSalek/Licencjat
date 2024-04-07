import pygame as pg
import sys
from SettingsMenu import settings_menu
import SETTINGS as S

# Klasy przycisków
class Button:
    def __init__(self, x, y, width, height, text, font, normal_color, hover_color, action=None):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.action = action
        self.hovered = False

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.normal_color
        pg.draw.rect(surface, color, self.rect)
        text_surface = self.font.render(self.text, True, S.BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

def draw_text(surface, text, color, x, y, font, center: bool):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# Funkcja wyświetlająca menu główne
def main_menu(screen, clock, client):
    # Czcionki
    text_font = pg.font.Font(None, 36)
    title_font = pg.font.Font(None, 94)

    # Zmienne do przycisków
    buttons_width = S.SCREEN_WIDTH/2
    buttons_height = S.SCREEN_HEIGHT/12
    first_pos_x = S.SCREEN_WIDTH/4
    first_pos_y = S.SCREEN_HEIGHT/4 + buttons_height
    buttons_padding = buttons_height * 1.5

    # Przyciski menu
    play_button = Button(first_pos_x, first_pos_y, buttons_width, buttons_height, "Online Game", text_font, S.GRAY, S.WHITE)
    settings_button = Button(first_pos_x, first_pos_y + buttons_padding, buttons_width, buttons_height, "Settings", text_font, S.GRAY, S.WHITE)
    how_to_button = Button(first_pos_x, first_pos_y + buttons_padding * 2, buttons_width, buttons_height, "How to play", text_font, S.GRAY, S.WHITE)
    quit_button = Button(first_pos_x, first_pos_y + buttons_padding * 3, buttons_width, buttons_height, "Quit", text_font, S.GRAY, S.WHITE)

    # Zmienne do pola na wpisywanie
    ibox_x = S.SCREEN_WIDTH * 3 / 5
    ibox_y = S.SCREEN_HEIGHT * 11 / 12
    ibox_width = S.SCREEN_WIDTH * 2 / 5 - 10
    ibox_height =  S.SCREEN_HEIGHT / 13 - 15
    ibox = pg.Rect(ibox_x, ibox_y, ibox_width, ibox_height)
    ibox_color_inactive = pg.Color('lightskyblue3')
    ibox_color_active = pg.Color('dodgerblue2')
    ibox_color = ibox_color_inactive
    ibox_active = False
    ibox_text = ''
    ibox_font = pg.font.Font(None, 28)
    text_font = pg.font.Font(None, 32)
    bad_keys = [pg.K_ESCAPE, pg.K_RETURN, pg.K_TAB, pg.K_SPACE, pg.K_DELETE, pg.K_KP_ENTER]

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button.rect.collidepoint(event.pos):
                        if len(ibox_text) != 0 and client.connect():
                            client.nickname = ibox_text
                            pass
                    elif settings_button.rect.collidepoint(event.pos):
                        settings_menu()
                    elif how_to_button.rect.collidepoint(event.pos):
                        pass
                    elif quit_button.rect.collidepoint(event.pos):
                        pg.quit()
                        sys.exit()
                    elif ibox.collidepoint(event.pos):
                        ibox_active = True
                    else:
                        ibox_active = False
                    ibox_color = ibox_color_active if ibox_active else ibox_color_inactive
            elif event.type == pg.KEYDOWN:
                if ibox_active:
                    if event.key == pg.K_BACKSPACE:
                        ibox_text = ibox_text[:-1]
                    else:
                        if len(ibox_text) < 16:
                            if event.unicode and event.key not in bad_keys:
                                ibox_text += event.unicode

        # Rysowanie menu
        screen.fill(S.BLACK)

        # Rysowanie tytułu
        draw_text(screen, "Gold & Treasures", S.YELLOW, S.SCREEN_WIDTH/2, S.SCREEN_HEIGHT/8, title_font, True)
        
        # Rysowanie przycisków
        play_button.draw(screen)
        settings_button.draw(screen)
        quit_button.draw(screen)
        how_to_button.draw(screen)

        # Rysowanie pola do wpisywania
        pg.draw.rect(screen, ibox_color, ibox, 2)
        pg.draw.rect(screen, S.WHITE, ibox.inflate(-4, -4))
        draw_text(screen, 'Nickname:', S.WHITE, ibox.x + 1, ibox.y - 30, text_font, False)
        draw_text(screen, ibox_text, S.BLACK, ibox.x + 5, ibox.y + 5, ibox_font, False)

        # Odświeżenie ekranu
        pg.display.flip()
        clock.tick(S.FPS)

        # Sprawdzenie najechania myszką
        mouse_pos = pg.mouse.get_pos()
        play_button.check_hover(mouse_pos)
        settings_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        how_to_button.check_hover(mouse_pos)

