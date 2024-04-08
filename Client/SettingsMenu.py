from UIComponents import draw_text, Button, Checkbox
import pygame as pg
import SETTINGS as S
import sys

def settings_menu(screen, clock):
    reinitialize = True
    options_changed = False

    resolution_option = S.RESOLUTION.index(S.WINDOW_SIZE)
    fps_option = S.CAN_FPS.index(S.FPS)


    while True:
        if reinitialize:
            # Czcionki
            button_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.04))
            text_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.03))
            title_font = pg.font.Font(S.FONT, int(S.SCREEN_WIDTH*0.1))

            # Przyciski menu
            back_button = Button(S.SCREEN_WIDTH/5, S.SCREEN_HEIGHT*11/13, S.SCREEN_WIDTH/5, S.SCREEN_HEIGHT/12, "Back", button_font, S.GRAY, S.WHITE)
            save_button = Button(S.SCREEN_WIDTH*3/5, S.SCREEN_HEIGHT*11/13, S.SCREEN_WIDTH/5, S.SCREEN_HEIGHT/12, "Save", button_font, S.GRAY, S.WHITE)
            arrow_width = S.SCREEN_WIDTH/12
            arrow_height = S.SCREEN_HEIGHT/12
            resolution_right_button = Button(S.SCREEN_WIDTH*18/20, S.SCREEN_HEIGHT*8/20, arrow_width, arrow_height, ">", button_font, S.GRAY, S.WHITE)
            resolution_left_button = Button(S.SCREEN_WIDTH*10/20, S.SCREEN_HEIGHT*8/20, arrow_width, arrow_height, "<", button_font, S.GRAY, S.WHITE)
            fps_right_button = Button(S.SCREEN_WIDTH*18/20, S.SCREEN_HEIGHT*10/20, arrow_width, arrow_height, ">", button_font, S.GRAY, S.WHITE)
            fps_left_button = Button(S.SCREEN_WIDTH*10/20, S.SCREEN_HEIGHT*10/20, arrow_width, arrow_height, "<", button_font, S.GRAY, S.WHITE)

            # Checkbox
            fullscreen_checkbox = Checkbox(screen, S.SCREEN_WIDTH*15/20, S.SCREEN_HEIGHT*6/20, arrow_height, S.GRAY, S.WHITE)
            fullscreen_checkbox.checked = S.FULLSCREEN

            buttons = [back_button, save_button, fps_left_button, fps_right_button, resolution_left_button, resolution_right_button]
            reinitialize = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_button.rect.collidepoint(event.pos):
                        return options_changed
                    elif fullscreen_checkbox.rect.collidepoint(event.pos):
                        fullscreen_checkbox.toggle()
                    elif resolution_left_button.rect.collidepoint(event.pos):
                        if resolution_option > 0:
                            resolution_option -= 1
                    elif resolution_right_button.rect.collidepoint(event.pos):
                        if resolution_option < len(S.RESOLUTION) - 1:
                            resolution_option += 1
                    elif fps_left_button.rect.collidepoint(event.pos):
                        if fps_option > 0:
                            fps_option -= 1
                    elif fps_right_button.rect.collidepoint(event.pos):
                        if fps_option < len(S.CAN_FPS) - 1:
                            fps_option += 1
                    elif save_button.rect.collidepoint(event.pos):
                        S.SCREEN_WIDTH = S.RESOLUTION[resolution_option][0]
                        S.SCREEN_HEIGHT = S.RESOLUTION[resolution_option][1]
                        S.WINDOW_SIZE = (S.SCREEN_WIDTH, S.SCREEN_HEIGHT)
                        S.FPS = S.CAN_FPS[fps_option]
                        S.FULLSCREEN = fullscreen_checkbox.checked
                        
                        if (S.FULLSCREEN and not pg.display.is_fullscreen) or (not S.FULLSCREEN and pg.display.is_fullscreen):
                            pg.display.toggle_fullscreen()

                        screen = pg.display.set_mode(S.WINDOW_SIZE)
                        

                        reinitialize = True
                        options_changed = True

        # Rysowanie menu
        screen.fill(S.BLACK)

        # Rysowanie tytułu
        draw_text(screen, "Settings", S.WHITE, S.SCREEN_WIDTH/2, S.SCREEN_HEIGHT/10, title_font, True)
        draw_text(screen, "Fullscreen", S.WHITE, S.SCREEN_WIDTH*6/20, S.SCREEN_HEIGHT*6/20+arrow_height/2, text_font, True)
        draw_text(screen, "Resolution", S.WHITE, S.SCREEN_WIDTH*6/20, S.SCREEN_HEIGHT*8/20+arrow_height/2, text_font, True)
        draw_text(screen, "FPS", S.WHITE, S.SCREEN_WIDTH*6/20, S.SCREEN_HEIGHT*10/20+arrow_height/2, text_font, True)
        resolution_text = str(S.RESOLUTION[resolution_option][0]) + "x" + str(S.RESOLUTION[resolution_option][1])
        draw_text(screen, resolution_text, S.WHITE, S.SCREEN_WIDTH*15/20, S.SCREEN_HEIGHT*8/20+arrow_height/2, text_font, True)
        draw_text(screen, str(S.CAN_FPS[fps_option]), S.WHITE, S.SCREEN_WIDTH*15/20, S.SCREEN_HEIGHT*10/20+arrow_height/2, text_font, True)

        # Rysowanie przycisków
        for button in buttons:
            button.draw(screen)

        fullscreen_checkbox.draw()

        # Odświeżenie ekranu
        pg.display.flip()
        clock.tick(S.FPS)

        # Sprawdzenie najechania myszką
        mouse_pos = pg.mouse.get_pos()
        for button in buttons:
            button.check_hover(mouse_pos)