from UIComponents import draw_text, Button
import pygame as pg
import SETTINGS as S
import sys

def settings_menu(screen, clock):
    # Czcionki
    button_font = pg.font.Font(S.FONT, 36)
    text_font = pg.font.Font(S.FONT, 28)
    title_font = pg.font.Font(S.FONT, 94)

    # Przyciski menu
    back_button = Button(S.SCREEN_WIDTH/5, S.SCREEN_HEIGHT*11/13, S.SCREEN_WIDTH/5, S.SCREEN_HEIGHT/12, "Back", button_font, S.GRAY, S.WHITE)
    save_button = Button(S.SCREEN_WIDTH*3/5, S.SCREEN_HEIGHT*11/13, S.SCREEN_WIDTH/5, S.SCREEN_HEIGHT/12, "Save", button_font, S.GRAY, S.WHITE)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_button.rect.collidepoint(event.pos):
                        return
                    if save_button.rect.collidepoint(event.pos):
                        pass

        # Rysowanie menu
        screen.fill(S.BLACK)

        # Rysowanie tytułu
        draw_text(screen, "How to play", S.WHITE, S.SCREEN_WIDTH/2, S.SCREEN_HEIGHT/8, title_font, True)
        
        # Rysowanie przycisków
        back_button.draw(screen)
        save_button.draw(screen)

        # Rysowanie tekstu how to play

        # Odświeżenie ekranu
        pg.display.flip()
        clock.tick(S.FPS)

        # Sprawdzenie najechania myszką
        mouse_pos = pg.mouse.get_pos()
        back_button.check_hover(mouse_pos)
        save_button.check_hover(mouse_pos)