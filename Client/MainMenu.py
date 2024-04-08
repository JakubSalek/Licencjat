import pygame as pg
import sys
from SettingsMenu import settings_menu
from HowToMenu import how_to_menu
import SETTINGS as S
from UIComponents import Button, draw_text

# Funkcja wyświetlająca menu główne
def main_menu(screen, clock, client):

    reinitialize = True

    

    while True:
        if reinitialize:
            # Czcionki
            text_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.04))
            title_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.1))

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
            ibox_font = pg.font.Font(None, 28)
            text_font = pg.font.Font(None, 32)
            ibox_x = S.SCREEN_WIDTH * 3 / 5
            ibox_y = S.SCREEN_HEIGHT * 11 / 12
            ibox_width = S.SCREEN_WIDTH * 2 / 5 - 10
            ibox_height = ibox_font.size("j")[1] * 1.5
            ibox = pg.Rect(ibox_x, ibox_y, ibox_width, ibox_height)
            ibox_color_inactive = pg.Color('lightskyblue3')
            ibox_color_active = pg.Color('dodgerblue2')
            ibox_color_failure = pg.Color(255, 0, 0)
            ibox_color = ibox_color_inactive
            ibox_active = False
            ibox_text = ''
            bad_keys = [pg.K_ESCAPE, pg.K_RETURN, pg.K_TAB, pg.K_SPACE, pg.K_DELETE, pg.K_KP_ENTER]

            reinitialize = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button.rect.collidepoint(event.pos):
                        if len(ibox_text) != 0 and ibox_text != "Can't connect to the server!":
                            client.nickname = ibox_text
                            connect = client.connect()
                            if connect == 0:
                                pass
                            else:
                                ibox_color = ibox_color_failure
                                ibox_text = "Can't connect to the server!"
                        else:
                            ibox_color = ibox_color_failure
                            ibox_text = ''
                    elif settings_button.rect.collidepoint(event.pos):
                        reinitialize = settings_menu(screen, clock)
                    elif how_to_button.rect.collidepoint(event.pos):
                        how_to_menu(screen, clock)
                    elif quit_button.rect.collidepoint(event.pos):
                        pg.quit()
                        sys.exit()
                    elif ibox.collidepoint(event.pos):
                        ibox_active = True
                        ibox_color = ibox_color_active
                        if ibox_text == "Can't connect to the server!":
                            ibox_text = ''
                    else:
                        ibox_active = False
                        ibox_color = ibox_color_inactive
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

