from GUI.UIComponents.TableBanerItem import TableBanerItem
from GUI.UIComponents.Button import Button
from GUI.TableMenu import TableMenu
from GUI.Menu import Menu
from Table import Table
from Player import Player
import pygame as pg
import SETTINGS as S

class ChooseTableMenu(Menu):
    def __init__(self, client, queue, clock, screen):
        super().__init__(client, queue, clock, screen)
        self.__tables = []
        self.__refresh_tables = True
        self.__sprite_items = []

        # Zmienne do przycisków
        buttons_width = S.SCREEN_WIDTH * 4/12
        buttons_height = S.SCREEN_HEIGHT/12

        # Przyciski menu
        self.__back_button = Button(S.SCREEN_WIDTH*1/12, S.SCREEN_HEIGHT*10/12, buttons_width,
                                    buttons_height, "Back", self._button_font)
        self.__create_button = Button(S.SCREEN_WIDTH*7/12, S.SCREEN_HEIGHT*10/12, buttons_width,
                                    buttons_height, "Create Table", self._button_font)
        
        self.__rect_width = S.SCREEN_WIDTH*0.9
        self.__rect_height = S.SCREEN_HEIGHT*9//12
        self.__tables_rect = pg.Rect(S.SCREEN_WIDTH*0.05, S.SCREEN_HEIGHT*0.05,
                                    self.__rect_width, S.SCREEN_HEIGHT*9/12) 
        
        self.__te_height = self.__rect_height//6

        self.__scroll = 0
        self.__button_scroll_speed = 5
        self.__mouse_scroll_speed = self.__button_scroll_speed * 5
        self.__scrollable_height = len(self.__tables) * self.__te_height - S.SCREEN_HEIGHT*9/12

    def run(self):
        self.__tables = []
        self.__refresh_tables = True
        self._client.send_menu("ChooseTableMenu")

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close_program()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.__create_button.check_click(event.pos):
                            self._client.create_table()
                        elif self.__back_button.check_click(event.pos):
                            self._client.send_menu("NONEED")
                            return
                        else:
                            for sprite in self.__sprite_items:
                                if sprite.check_click(event.pos):
                                    self._client.join_table(sprite.get_table())
                                    TableMenu(self._client, self._message_queue, self._clock, self._screen, sprite.get_table(), False)
                                    self.clear_and_ask()
                    elif event.button == 4:
                        self.__scroll -= self.__mouse_scroll_speed if self.__scroll > 0 else 0
                        self.__refresh_tables = True
                    elif event.button == 5:
                        self.__scroll += self.__mouse_scroll_speed if self.__scroll < self.__scrollable_height else 0
                        self.__refresh_tables = True
            keys = pg.key.get_pressed()
            if keys[pg.K_UP]:
                self.__scroll -= self.__button_scroll_speed if self.__scroll > 0 else 0
                self.__refresh_tables = True
            elif keys[pg.K_DOWN]:
                self.__scroll += self.__button_scroll_speed if self.__scroll < self.__scrollable_height else 0
                self.__refresh_tables = True
        
            self.draw()
            self.check_server()

    def draw(self):
        # Rysowanie menu
        self._screen.fill(S.BLACK)

        # Rysowanie stolików
        pg.draw.rect(self._screen, S.WHITE, self.__tables_rect, 2)
 
        if self.__refresh_tables:
            self.__sprite_items = []
            for i, table in enumerate(self.__tables):
                table_rect = pg.Rect(self.__tables_rect.left, self.__tables_rect.top + i * self.__te_height - self.__scroll,
                                    self.__rect_width, self.__te_height)
                if self.__tables_rect.contains(table_rect):
                    table_sprite = TableBanerItem(table, self._text_font, self.__rect_width, self.__te_height)
                    table_sprite.set_rect(table_rect)
                    self.__sprite_items.append(table_sprite)
            self.__refresh_tables = False

        for sprite in self.__sprite_items:
            sprite.draw()
            self._screen.blit(sprite.get_surface(), sprite.get_rect())

        # Rysowanie przycisków
        self.__back_button.draw(self._screen)
        self.__create_button.draw(self._screen)

        # Odświeżenie ekranu
        pg.display.flip()
        self._clock.tick(S.FPS)

        # Sprawdzenie najechania myszką
        mouse_pos = pg.mouse.get_pos()
        self.__back_button.check_hover(mouse_pos)
        self.__create_button.check_hover(mouse_pos)
        for sprite in self.__sprite_items:
            sprite.check_hover(mouse_pos)


    def reinitialize_menu(self):
        # Zmienne do przycisków
        buttons_width = S.SCREEN_WIDTH * 4/12
        buttons_height = S.SCREEN_HEIGHT/12

        # Przyciski menu
        self.__back_button = Button(S.SCREEN_WIDTH*1/12, S.SCREEN_HEIGHT*10/12, buttons_width,
                                    buttons_height, "Back", self._button_font)
        self.__create_button = Button(S.SCREEN_WIDTH*7/12, S.SCREEN_HEIGHT*10/12, buttons_width,
                                    buttons_height, "Create Table", self._button_font)
        
        self.__rect_width = S.SCREEN_WIDTH*0.9
        self.__rect_height = S.SCREEN_HEIGHT*9//12
        self.__tables_rect = pg.Rect(S.SCREEN_WIDTH*0.05, S.SCREEN_HEIGHT*0.05,
                                    self.__rect_width, S.SCREEN_HEIGHT*9/12) 
        
        self.__te_height = self.__rect_height//6

        self.__scroll = 0
        self.__button_scroll_speed = 5
        self.__mouse_scroll_speed = self.__button_scroll_speed * 5
        self.__scrollable_height = len(self.__tables) * self.__te_height - S.SCREEN_HEIGHT*9/12

    
    def check_server(self):
        while not self._message_queue.empty():
            message: str = self._message_queue.get_nowait()
            
            if message.startswith("Table"):
                _, id, name, player_count, started = message.split(";")
                found = False
                for table in self.__tables:
                    if table.get_id() == id:
                        table.set_player_count(player_count)
                        found = True
                if not found:
                    self.__tables.append(Table(id, name, player_count, int(started)))
                self.__scrollable_height = len(self.__tables) * self.__te_height - S.SCREEN_HEIGHT*9/12
                self.__refresh_tables = True
            elif message.startswith("CreateTable"):
                _, id, name = message.split(";")
                my_table = Table(id, name, 1, False)
                my_table.add_player(Player(self._client.get_id(), self._client.get_nickname(), S.PLAYER_COLORS[0]))
                TableMenu(self._client, self._message_queue, self._clock, self._screen, my_table, True)
                self.clear_and_ask()
            elif message.startswith("DeleteTable"):
                _, id = message.split(";")
                for table in self.__tables:
                    if table.get_id() == id:
                        self.__tables.remove(table)
                        self.__refresh_tables = True
                        break
            elif message.startswith("StartTable"):
                _, id = message.split(";")
                for table in self.__tables:
                    if table.get_id() == id:
                        table.set_started(True)
                        self.__refresh_tables = True
                        break
            else:
                print(f"Unhandled message \"{message}\"") if S.DEBUG else None

    def clear_and_ask(self):
        self.__tables = []
        self.__refresh_tables = True
        self._client.send_menu("ChooseTableMenu")

    def close_program(self):
        return super().close_program()