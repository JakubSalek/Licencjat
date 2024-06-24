from GUI.UIComponents.TextFunctions import draw_text, read_text_from_file, render_text_scrolled
from GUI.UIComponents.Button import Button
from GUI.Menu import Menu
import pygame as pg
import SETTINGS as S

class HowToMenu(Menu):
    def __init__(self, client, queue, clock, screen):
        super().__init__(client, queue, clock, screen)    

        self.__back_button = Button(S.SCREEN_WIDTH/4, S.SCREEN_HEIGHT*7/8, S.SCREEN_WIDTH/2,
                                    S.SCREEN_HEIGHT/12, "Back", self._button_font)
  
        # Zmienne do przewijanego tekstu
        self.__text = read_text_from_file(S.HOW_TO_FILE)
        text_area_width = S.SCREEN_WIDTH*4/5
        text_area_height = S.SCREEN_HEIGHT*9/15
        self.__text_padding = 10
        self.__line_spacing = 5
        self.__scroll = 0
        self.__button_scroll_speed = 5
        self.__mouse_scroll_speed = self.__button_scroll_speed * 10
        self.__text_rect = pg.Rect((S.SCREEN_WIDTH - text_area_width) // 2,
                                  (S.SCREEN_HEIGHT - text_area_height) // 2,
                                    text_area_width, text_area_height)

    def run(self):
        # Główna pętla menu
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close_program()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.__back_button.check_click(event.pos):
                            return
                    elif event.button == 4:
                        self.__scroll -= self.__mouse_scroll_speed
                    elif event.button == 5:
                        self.__scroll += self.__mouse_scroll_speed
            keys = pg.key.get_pressed()
            if keys[pg.K_UP]:
                self.__scroll -= self.__button_scroll_speed
            elif keys[pg.K_DOWN]:
                self.__scroll += self.__button_scroll_speed
            
            self.draw()
            self.check_server()

    def draw(self):
        # Rysowanie menu
        self._screen.fill(S.BG_COLOR)

        # Rysowanie tytułu
        draw_text(self._screen, "How to play", S.FONT_COLOR, S.SCREEN_WIDTH/2,
                  S.SCREEN_HEIGHT/10, self._title_font, True)
        
        # Rysowanie przycisków
        self.__back_button.draw(self._screen)

        # Rysowanie tekstu how to play
        if self.__scroll < 0:
            self.__scroll = 0

        pg.draw.rect(self._screen, S.WHITE, self.__text_rect, 2)
        render_text_scrolled(self._screen, self._text_font, self.__text, self.__scroll,
                             S.FONT_COLOR, self.__line_spacing, self.__text_rect, self.__text_padding)

        # Odświeżenie ekranu
        pg.display.flip()
        self._clock.tick(S.FPS)

        # Sprawdzenie najechania myszką
        mouse_pos = pg.mouse.get_pos()
        self.__back_button.check_hover(mouse_pos)


    def reinitialize_menu(self):
        self.__back_button = Button(S.SCREEN_WIDTH/4, S.SCREEN_HEIGHT*7/8, S.SCREEN_WIDTH/2,
                                    S.SCREEN_HEIGHT/12, "Back", self._button_font)
  
        # Zmienne do przewijanego tekstu
        self.__text = read_text_from_file(S.HOW_TO_FILE)
        text_area_width = S.SCREEN_WIDTH*4/5
        text_area_height = S.SCREEN_HEIGHT*9/15
        self.__text_padding = 10
        self.__line_spacing = 5
        self.__scroll = 0
        self.__button_scroll_speed = 5
        self.__mouse_scroll_speed = self.__button_scroll_speed * 10
        self.__text_rect = pg.Rect((S.SCREEN_WIDTH - text_area_width) // 2,
                                  (S.SCREEN_HEIGHT - text_area_height) // 2,
                                    text_area_width, text_area_height)

    def check_server(self):
        while not self._message_queue.empty():
            message = self._message_queue.get_nowait()
            print(f"Unhandled message \"{message}\"") if S.DEBUG else None
            
    def close_program(self):
        return super().close_program()