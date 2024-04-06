import pygame as pg
import sys
import SETTINGS as S


# Funkcja rysująca tekst na ekranie
def draw_text(surface, text, color, x, y, font):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# Funkcja główna menu
def welcome_menu(screen, clock, client):
    ibox = pg.Rect(S.SCREEN_WIDTH/4 , S.SCREEN_HEIGHT/2, S.SCREEN_WIDTH/2, 28)
    ibox_color_inactive = pg.Color('lightskyblue3')
    ibox_color_active = pg.Color('dodgerblue2')
    ibox_color = ibox_color_inactive
    ibox_active = False
    ibox_text = ''
    ibox_font = pg.font.Font(None, 28)
    text_font = pg.font.Font(None, 32)
    bad_keys = [pg.K_ESCAPE, pg.K_RETURN, pg.K_TAB, pg.K_SPACE, pg.K_DELETE, pg.K_KP_ENTER]

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if ibox.collidepoint(event.pos):
                    ibox_active = True
                else:
                    ibox_active = False
                ibox_color = ibox_color_active if ibox_active else ibox_color_inactive
            if event.type == pg.KEYDOWN:
                if ibox_active:
                    if event.key == pg.K_RETURN and len(ibox_text) != 0:
                        client.nickname = ibox_text
                        return
                    elif event.key == pg.K_BACKSPACE:
                        ibox_text = ibox_text[:-1]
                    else:
                        if len(ibox_text) < 16:
                            if event.unicode and event.key not in bad_keys:
                                ibox_text += event.unicode

        screen.fill(S.WHITE)
        pg.draw.rect(screen, ibox_color, ibox, 2)
        draw_text(screen, 'Nickname:', S.TEXT_COLOR, ibox.x, ibox.y - 30, text_font)
        draw_text(screen, ibox_text, S.TEXT_COLOR, ibox.x + 5, ibox.y + 5, ibox_font)
        pg.display.flip()
        clock.tick(S.FPS)
