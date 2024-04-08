from UIComponents import draw_text, Button, read_text_from_file, render_text_scrolled
import pygame as pg
import SETTINGS as S
import sys

def how_to_menu(screen, clock):
    # Czcionki
    button_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.04))
    text_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.03))
    title_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.1))

    # Przyciski menu
    back_button = Button(S.SCREEN_WIDTH/4, S.SCREEN_HEIGHT*7/8, S.SCREEN_WIDTH/2, S.SCREEN_HEIGHT/12, "Back", button_font, S.GRAY, S.WHITE)
  
    # Zmienne do przewijanego tekstu
    text = read_text_from_file(S.HOW_TO_FILE)
    text_area_width = S.SCREEN_WIDTH*4/5
    text_area_height = S.SCREEN_HEIGHT*9/15
    text_padding = 10
    line_spacing = 5
    scroll = 0
    button_scroll_speed = 5
    mouse_scroll_speed = button_scroll_speed * 10
    text_rect = pg.Rect((S.SCREEN_WIDTH - text_area_width) // 2, (S.SCREEN_HEIGHT - text_area_height) // 2, text_area_width, text_area_height)


    # Główna pętla menu
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_button.rect.collidepoint(event.pos):
                        return
                elif event.button == 4:
                    scroll -= mouse_scroll_speed
                elif event.button == 5:
                    scroll += mouse_scroll_speed
                    
        # Sprawdzenie czy chcemy przewijać
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            scroll -= button_scroll_speed
        elif keys[pg.K_DOWN]:
            scroll += button_scroll_speed

        # Rysowanie menu
        screen.fill(S.BLACK)

        # Rysowanie tytułu
        draw_text(screen, "How to play", S.WHITE, S.SCREEN_WIDTH/2, S.SCREEN_HEIGHT/10, title_font, True)
        
        # Rysowanie przycisków
        back_button.draw(screen)

        # Rysowanie tekstu how to play
        if scroll < 0:
            scroll = 0


        pg.draw.rect(screen, S.WHITE, text_rect, 2)
        render_text_scrolled(screen, text_font, text, scroll, S.WHITE, line_spacing, text_rect, text_padding)

        # Odświeżenie ekranu
        pg.display.flip()
        clock.tick(S.FPS)

        # Sprawdzenie najechania myszką
        mouse_pos = pg.mouse.get_pos()
        back_button.check_hover(mouse_pos)