from GUI.UIComponents import draw_text, Button, read_text_from_file, render_text_scrolled
import pygame as pg
from GUI.Menu import Menu
import SETTINGS as S
import sys


class HowToMenu(Menu):
    def __init__(self, gui):
        super().__init__(gui)    
        self.back_button = Button(S.SCREEN_WIDTH/4, S.SCREEN_HEIGHT*7/8, S.SCREEN_WIDTH/2,
                                S.SCREEN_HEIGHT/12, "Back", self.gui.button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
  
        # Zmienne do przewijanego tekstu
        self.text = read_text_from_file(S.HOW_TO_FILE)
        self.text_area_width = S.SCREEN_WIDTH*4/5
        self.text_area_height = S.SCREEN_HEIGHT*9/15
        self.text_padding = 10
        self.line_spacing = 5
        self.scroll = 0
        self.button_scroll_speed = 5
        self.mouse_scroll_speed = self.button_scroll_speed * 10
        self.text_rect = pg.Rect((S.SCREEN_WIDTH - self.text_area_width) // 2, (S.SCREEN_HEIGHT - self.text_area_height) // 2, self.text_area_width, self.text_area_height)

    def run(self):
        # Główna pętla menu
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close_program()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.back_button.rect.collidepoint(event.pos):
                            return
                    elif event.button == 4:
                        self.scroll -= self.mouse_scroll_speed
                    elif event.button == 5:
                        self.scroll += self.mouse_scroll_speed
            keys = pg.key.get_pressed()
            if keys[pg.K_UP]:
                self.scroll -= self.button_scroll_speed
            elif keys[pg.K_DOWN]:
                self.scroll += self.button_scroll_speed
            
            self.draw()
            self.check_server()

    def draw(self):
        self.reinitialize_menu() if self.reinitialize else None

        screen = self.gui.screen
        clock = self.gui.clock
        text_font = self.gui.text_font
        title_font = self.gui.title_font

        # Rysowanie menu
        screen.fill(S.BG_COLOR)

        # Rysowanie tytułu
        draw_text(screen, "How to play", S.FONT_COLOR, S.SCREEN_WIDTH/2, S.SCREEN_HEIGHT/10, title_font, True)
        
        # Rysowanie przycisków
        self.back_button.draw(screen)

        # Rysowanie tekstu how to play
        if self.scroll < 0:
            self.scroll = 0

        pg.draw.rect(screen, S.WHITE, self.text_rect, 2)
        render_text_scrolled(screen, text_font, self.text, self.scroll, S.FONT_COLOR, self.line_spacing, self.text_rect, self.text_padding)

        # Odświeżenie ekranu
        pg.display.flip()
        clock.tick(S.FPS)

        # Sprawdzenie najechania myszką
        mouse_pos = pg.mouse.get_pos()
        self.back_button.check_hover(mouse_pos)


    def reinitialize_menu(self):
        self.back_button = Button(S.SCREEN_WIDTH/4, S.SCREEN_HEIGHT*7/8, S.SCREEN_WIDTH/2, S.SCREEN_HEIGHT/12, "Back", self.gui.button_font, S.GRAY, S.WHITE)
  
        # Zmienne do przewijanego tekstu
        self.text_area_width = S.SCREEN_WIDTH*4/5
        self.text_area_height = S.SCREEN_HEIGHT*9/15
        self.text_rect = pg.Rect((S.SCREEN_WIDTH - self.text_area_width) // 2, (S.SCREEN_HEIGHT - self.text_area_height) // 2, self.text_area_width, self.text_area_height)

        self.reinitialize = False

    def check_server(self):
        while not self.gui.message_queue.empty():
            message = self.gui.message_queue.get_nowait()
            
    def close_program(self):
        return super().close_program()