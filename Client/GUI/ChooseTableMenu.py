import pygame as pg
from GUI.Menu import Menu
from GUI.TableMenu import TableMenu
from GUI.UIComponents import Button, draw_text
from Table import Table
from Player import Player
import SETTINGS as S

class TableItem():
    def __init__(self, table, font, width, height):
        self.swidth = width
        self.sheight = height
        self.surface = pg.Surface((width, height))
        self.surface.fill(S.BETTER_GRAY)
        self.table = table
        self.font = font
        self.rect = self.surface.get_rect()
        self.button = Button(self.swidth*0.75, self.sheight*0.25, self.swidth*0.15, self.sheight*0.5,
                            "Join", self.font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
        if self.table.curr_players == "4" or self.table.is_started:
            self.button.active = False

    def draw(self):
        self.surface.fill(S.BETTER_GRAY)
        draw_text(self.surface, str(self.table.id), S.FONT_COLOR2, self.swidth*0.05, self.sheight*0.5, self.font, True)
        draw_text(self.surface, str(self.table.name), S.FONT_COLOR2, self.swidth*0.35, self.sheight*0.5, self.font, True)
        draw_text(self.surface, f"{str(self.table.curr_players)}/4", S.FONT_COLOR2, self.swidth*0.65, self.sheight*0.5, self.font, True)
        self.button.draw(self.surface)

    def get_button(self):
        return self.button

class ChooseTableMenu(Menu):
    def __init__(self, gui):
        super().__init__(gui)
        self.tables = []
        self.refresh_tables = True
        self.sprite_items = []

        # Zmienne do przycisków
        self.buttons_width = S.SCREEN_WIDTH * 4/12
        self.buttons_height = S.SCREEN_HEIGHT/12

        # Przyciski menu
        self.back_button = Button(S.SCREEN_WIDTH*1/12, S.SCREEN_HEIGHT*10/12, self.buttons_width,
                                self.buttons_height, "Back", self.gui.button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
        self.create_button = Button(S.SCREEN_WIDTH*7/12, S.SCREEN_HEIGHT*10/12, self.buttons_width,
                                self.buttons_height, "Create Table", self.gui.button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
        
        self.rect_width = S.SCREEN_WIDTH*0.9
        self.rect_height = S.SCREEN_HEIGHT*9//12
        self.tables_rect = pg.Rect(S.SCREEN_WIDTH*0.05, S.SCREEN_HEIGHT*0.05,
                                    self.rect_width, S.SCREEN_HEIGHT*9/12) 
        
        self.te_height = self.rect_height//6

        self.scroll = 0
        self.button_scroll_speed = 5
        self.mouse_scroll_speed = self.button_scroll_speed * 5
        self.scrollable_height = len(self.tables) * self.te_height - S.SCREEN_HEIGHT*9/12

    def run(self):
        self.tables = []
        self.refresh_tables = True
        self.gui.client.send_menu("ChooseTableMenu")

        while True:
            self.reinitialize_menu() if self.reinitialize else None

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close_program()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.create_button.rect.collidepoint(event.pos):
                            self.gui.client.create_table()
                        elif self.back_button.rect.collidepoint(event.pos):
                            self.gui.client.send_menu("NONEED")
                            return
                        else:
                            for sprite in self.sprite_items:
                                if sprite.button.active:
                                    x, y = event.pos
                                    x -= sprite.rect.left
                                    y -= sprite.rect.top
                                    if sprite.button.rect.collidepoint((x, y)):
                                        self.gui.client.join_table(sprite.table)
                                        TableMenu(self.gui, sprite.table, False)
                                        self.clear_and_ask()
                    elif event.button == 4:
                        self.scroll -= self.mouse_scroll_speed if self.scroll > 0 else 0
                        self.refresh_tables = True
                    elif event.button == 5:
                        self.scroll += self.mouse_scroll_speed if self.scroll < self.scrollable_height else 0
                        self.refresh_tables = True
            keys = pg.key.get_pressed()
            if keys[pg.K_UP]:
                self.scroll -= self.button_scroll_speed if self.scroll > 0 else 0
                self.refresh_tables = True
            elif keys[pg.K_DOWN]:
                self.scroll += self.button_scroll_speed if self.scroll < self.scrollable_height else 0
                self.refresh_tables = True
        
            self.draw()
            self.check_server()

    def draw(self):
        # Pomocnicze zmienne
        screen = self.gui.screen

        # Rysowanie menu
        screen.fill(S.BLACK)

        # Rysowanie stolików
        pg.draw.rect(screen, S.WHITE, self.tables_rect, 2)
 
        if self.refresh_tables:
            self.sprite_items = []
            for i, table in enumerate(self.tables):
                table_rect = pg.Rect(self.tables_rect.left, self.tables_rect.top + i * self.te_height - self.scroll,
                                    self.rect_width, self.te_height)
                if self.tables_rect.contains(table_rect):
                    table_sprite = TableItem(table, self.gui.xs_font, self.rect_width, self.te_height)
                    table_sprite.rect = table_rect
                    self.sprite_items.append(table_sprite)
            self.refresh_tables = False

        for sprite in self.sprite_items:
            sprite.draw()
            screen.blit(sprite.surface, sprite.rect)

        # Rysowanie przycisków
        self.back_button.draw(screen)
        self.create_button.draw(screen)

        # Odświeżenie ekranu
        pg.display.flip()
        self.gui.clock.tick(S.FPS)

        # Sprawdzenie najechania myszką
        mouse_pos = pg.mouse.get_pos()
        self.back_button.check_hover(mouse_pos)
        self.create_button.check_hover(mouse_pos)
        for sprite in self.sprite_items:
            if sprite.button.active:
                x, y = mouse_pos
                x -= sprite.rect.left
                y -= sprite.rect.top
                sprite.button.check_hover((x, y))


    def reinitialize_menu(self):
        # Zmienne do przycisków
        self.buttons_width = S.SCREEN_WIDTH * 4/12
        self.buttons_height = S.SCREEN_HEIGHT/12

        # Przyciski menu
        self.back_button = Button(S.SCREEN_WIDTH*1/12, S.SCREEN_HEIGHT*10/12, self.buttons_width,
                                self.buttons_height, "Back", self.gui.button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
        self.create_button = Button(S.SCREEN_WIDTH*7/12, S.SCREEN_HEIGHT*10/12, self.buttons_width,
                                self.buttons_height, "Create Table", self.gui.button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
        
        self.rect_width = S.SCREEN_WIDTH*0.9
        self.rect_height = S.SCREEN_HEIGHT*9//12
        self.tables_rect = pg.Rect(S.SCREEN_WIDTH*0.05, S.SCREEN_HEIGHT*0.05,
                                    self.rect_width, S.SCREEN_HEIGHT*9/12) 
        
        self.te_height = self.rect_height//6

        self.mouse_scroll_speed = self.button_scroll_speed * 5
        self.scrollable_height = len(self.tables) * self.te_height - S.SCREEN_HEIGHT*9/12

        self.reinitialize = False

    
    def check_server(self):
        while not self.gui.message_queue.empty():
            message: str = self.gui.message_queue.get_nowait()
            
            if message.startswith("Table"):
                _, id, name, curr_players, started = message.split(";")
                found = False
                for table in self.tables:
                    if table.id == id:
                        table.name = name
                        table.curr_players = curr_players
                        found = True
                if not found:
                    self.tables.append(Table(id, name, curr_players, int(started)))
                self.scrollable_height = len(self.tables) * self.te_height - S.SCREEN_HEIGHT*9/12
                self.refresh_tables = True
            elif message.startswith("CreateTable"):
                _, id, name = message.split(";")
                my_table = Table(id, name, 1, False)
                my_table.players = [Player(self.gui.client.id, self.gui.client.nickname)]
                TableMenu(self.gui, my_table, True)
                self.clear_and_ask()
            elif message.startswith("DeleteTable"):
                _, id = message.split(";")
                for table in self.tables:
                    if table.id == id:
                        self.tables.remove(table)
                        self.refresh_tables = True
                        break
            elif message.startswith("StartTable"):
                _, id = message.split(";")
                for table in self.tables:
                    if table.id == id:
                        table.is_started = True
                        self.refresh_tables = True
                        break
            else:
                print(f"Unhandled message \"{message}\"") if S.DEBUG else None

    def clear_and_ask(self):
        self.tables = []
        self.refresh_tables = True
        self.gui.client.send_menu("ChooseTableMenu")

    def close_program(self):
        return super().close_program()